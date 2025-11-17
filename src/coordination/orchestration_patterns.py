"""Orchestration Patterns for Multi-Agent Coordination.

This module provides different coordination patterns for organizing agent collaboration:
- Hierarchical: Manager-worker pattern with task delegation
- Pipeline: Sequential processing with data flow between agents
- Peer-to-Peer: Decentralized collaboration between equal agents
"""

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple
import logging

from .a2a_protocol import A2AMessage, MessageType
from .message_broker import MessageBroker


logger = logging.getLogger(__name__)


@dataclass
class OrchestrationResult:
    """Result of an orchestration execution.

    Attributes:
        success: Whether the orchestration completed successfully
        results: Results from each agent/stage
        errors: Any errors that occurred
        metadata: Additional metadata about the execution
    """

    success: bool
    results: Dict[str, Any]
    errors: List[str]
    metadata: Dict[str, Any]


class OrchestrationPattern(ABC):
    """Base class for orchestration patterns."""

    def __init__(self, broker: MessageBroker):
        """Initialize the orchestration pattern.

        Args:
            broker: Message broker for agent communication
        """
        self.broker = broker
        self._orchestration_id = None

    @abstractmethod
    async def execute(self, *args, **kwargs) -> OrchestrationResult:
        """Execute the orchestration pattern.

        Returns:
            OrchestrationResult with execution details
        """
        pass


class HierarchicalPattern(OrchestrationPattern):
    """Hierarchical orchestration pattern (Manager-Worker).

    A manager agent delegates tasks to multiple worker agents and aggregates results.
    Supports:
    - Task distribution
    - Result aggregation
    - Worker failure handling
    - Dynamic worker pool
    """

    def __init__(
        self,
        broker: MessageBroker,
        manager_id: str,
        worker_ids: List[str],
        aggregation_fn: Optional[Callable] = None,
    ):
        """Initialize hierarchical pattern.

        Args:
            broker: Message broker instance
            manager_id: ID of the manager agent
            worker_ids: List of worker agent IDs
            aggregation_fn: Function to aggregate worker results
        """
        super().__init__(broker)
        self.manager_id = manager_id
        self.worker_ids = worker_ids
        self.aggregation_fn = aggregation_fn or self._default_aggregation

    @staticmethod
    def _default_aggregation(results: Dict[str, Any]) -> Any:
        """Default aggregation function that returns all results as a dict.

        Args:
            results: Dictionary of worker_id -> result

        Returns:
            The results dictionary
        """
        return results

    async def execute(
        self,
        task: Dict[str, Any],
        timeout: float = 30.0,
        require_all: bool = True,
    ) -> OrchestrationResult:
        """Execute hierarchical orchestration.

        Args:
            task: Task description to distribute to workers
            timeout: Maximum time to wait for worker responses
            require_all: Whether all workers must respond successfully

        Returns:
            OrchestrationResult with aggregated worker results
        """
        logger.info(
            f"Starting hierarchical orchestration: manager={self.manager_id}, "
            f"workers={len(self.worker_ids)}"
        )

        results = {}
        errors = []
        conversation_id = f"hierarchical-{id(self)}"

        # Subscribe manager to responses
        manager_queue = await self.broker.subscribe(
            self.manager_id,
            message_types=[MessageType.TASK_COMPLETION, MessageType.TASK_FAILURE],
        )

        try:
            # Assign tasks to workers
            for worker_id in self.worker_ids:
                message = A2AMessage(
                    conversation_id=conversation_id,
                    from_agent_id=self.manager_id,
                    to_agent_id=worker_id,
                    message_type=MessageType.TASK_ASSIGNMENT,
                    payload={"task": task, "worker_id": worker_id},
                    requires_response=True,
                )
                await self.broker.publish(message)
                logger.debug(f"Assigned task to worker {worker_id}")

            # Collect responses from workers
            pending_workers = set(self.worker_ids)
            start_time = asyncio.get_event_loop().time()

            while pending_workers and (asyncio.get_event_loop().time() - start_time) < timeout:
                try:
                    # Wait for next message with remaining timeout
                    remaining_timeout = timeout - (asyncio.get_event_loop().time() - start_time)
                    message = await asyncio.wait_for(
                        manager_queue.get(),
                        timeout=max(0.1, remaining_timeout),
                    )

                    if message.conversation_id != conversation_id:
                        continue

                    worker_id = message.from_agent_id

                    if message.message_type == MessageType.TASK_COMPLETION:
                        results[worker_id] = message.payload.get("result")
                        pending_workers.discard(worker_id)
                        logger.debug(f"Received completion from worker {worker_id}")

                    elif message.message_type == MessageType.TASK_FAILURE:
                        error_msg = f"Worker {worker_id} failed: {message.payload.get('error')}"
                        errors.append(error_msg)
                        pending_workers.discard(worker_id)
                        logger.warning(error_msg)

                except asyncio.TimeoutError:
                    break

            # Check for timeout workers
            if pending_workers:
                timeout_msg = f"Workers timed out: {pending_workers}"
                errors.append(timeout_msg)
                logger.warning(timeout_msg)

            # Determine success
            success = (not require_all and len(results) > 0) or (require_all and len(pending_workers) == 0)

            # Aggregate results
            aggregated_result = None
            if results:
                try:
                    aggregated_result = self.aggregation_fn(results)
                except Exception as e:
                    errors.append(f"Aggregation failed: {str(e)}")
                    logger.error(f"Aggregation failed: {e}")

            return OrchestrationResult(
                success=success,
                results={
                    "individual_results": results,
                    "aggregated_result": aggregated_result,
                    "completed_workers": len(results),
                    "total_workers": len(self.worker_ids),
                },
                errors=errors,
                metadata={
                    "pattern": "hierarchical",
                    "manager_id": self.manager_id,
                    "worker_ids": self.worker_ids,
                    "conversation_id": conversation_id,
                },
            )

        finally:
            await self.broker.unsubscribe(self.manager_id)


class PipelinePattern(OrchestrationPattern):
    """Pipeline orchestration pattern.

    Data flows sequentially through a series of agent stages, where each stage
    processes the output of the previous stage.
    Supports:
    - Sequential processing
    - Data transformation at each stage
    - Stage failure handling
    - Pipeline metrics
    """

    def __init__(
        self,
        broker: MessageBroker,
        stages: List[Tuple[str, Callable]],
    ):
        """Initialize pipeline pattern.

        Args:
            broker: Message broker instance
            stages: List of (agent_id, processing_function) tuples defining the pipeline
        """
        super().__init__(broker)
        self.stages = stages

    async def execute(
        self,
        initial_input: Any,
        timeout_per_stage: float = 30.0,
    ) -> OrchestrationResult:
        """Execute pipeline orchestration.

        Args:
            initial_input: Initial input to the pipeline
            timeout_per_stage: Maximum time to wait for each stage

        Returns:
            OrchestrationResult with final output and stage results
        """
        logger.info(f"Starting pipeline orchestration with {len(self.stages)} stages")

        stage_results = {}
        errors = []
        conversation_id = f"pipeline-{id(self)}"
        current_data = initial_input

        for stage_idx, (agent_id, process_fn) in enumerate(self.stages):
            stage_name = f"stage_{stage_idx}_{agent_id}"
            logger.debug(f"Executing {stage_name}")

            try:
                # Subscribe to this stage's output
                stage_queue = await self.broker.subscribe(
                    f"pipeline-coordinator-{stage_idx}",
                    message_types=[MessageType.TASK_COMPLETION, MessageType.TASK_FAILURE],
                )

                # Send data to stage agent
                message = A2AMessage(
                    conversation_id=conversation_id,
                    from_agent_id=f"pipeline-coordinator",
                    to_agent_id=agent_id,
                    message_type=MessageType.TASK_ASSIGNMENT,
                    payload={"input": current_data, "stage": stage_idx},
                    requires_response=True,
                )
                await self.broker.publish(message)

                # Wait for stage completion
                try:
                    response = await asyncio.wait_for(
                        stage_queue.get(),
                        timeout=timeout_per_stage,
                    )

                    if response.message_type == MessageType.TASK_COMPLETION:
                        # Process the output with the stage function
                        stage_output = process_fn(response.payload.get("result", current_data))
                        stage_results[stage_name] = stage_output
                        current_data = stage_output
                        logger.debug(f"Completed {stage_name}")

                    elif response.message_type == MessageType.TASK_FAILURE:
                        error_msg = f"{stage_name} failed: {response.payload.get('error')}"
                        errors.append(error_msg)
                        logger.error(error_msg)
                        break

                except asyncio.TimeoutError:
                    error_msg = f"{stage_name} timed out"
                    errors.append(error_msg)
                    logger.error(error_msg)
                    break

                finally:
                    await self.broker.unsubscribe(f"pipeline-coordinator-{stage_idx}")

            except Exception as e:
                error_msg = f"{stage_name} error: {str(e)}"
                errors.append(error_msg)
                logger.error(error_msg)
                break

        success = len(errors) == 0 and len(stage_results) == len(self.stages)

        return OrchestrationResult(
            success=success,
            results={
                "final_output": current_data,
                "stage_results": stage_results,
                "stages_completed": len(stage_results),
                "total_stages": len(self.stages),
            },
            errors=errors,
            metadata={
                "pattern": "pipeline",
                "conversation_id": conversation_id,
                "stages": [agent_id for agent_id, _ in self.stages],
            },
        )


class PeerToPeerPattern(OrchestrationPattern):
    """Peer-to-Peer orchestration pattern.

    Agents collaborate as equals without a central coordinator, using consensus
    or voting mechanisms to make decisions.
    Supports:
    - Decentralized decision making
    - Voting/consensus mechanisms
    - Peer discovery
    - Conflict resolution
    """

    def __init__(
        self,
        broker: MessageBroker,
        peer_ids: List[str],
        consensus_threshold: float = 0.5,
    ):
        """Initialize peer-to-peer pattern.

        Args:
            broker: Message broker instance
            peer_ids: List of peer agent IDs
            consensus_threshold: Fraction of peers needed for consensus (0.0-1.0)
        """
        super().__init__(broker)
        self.peer_ids = peer_ids
        self.consensus_threshold = consensus_threshold

    async def execute(
        self,
        proposal: Dict[str, Any],
        timeout: float = 30.0,
        voting_round_id: Optional[str] = None,
    ) -> OrchestrationResult:
        """Execute peer-to-peer orchestration with voting.

        Args:
            proposal: Proposal to vote on
            timeout: Maximum time to wait for votes
            voting_round_id: Optional ID for this voting round

        Returns:
            OrchestrationResult with voting results and consensus status
        """
        voting_round_id = voting_round_id or f"p2p-{id(self)}"
        logger.info(
            f"Starting P2P orchestration: voting_round={voting_round_id}, "
            f"peers={len(self.peer_ids)}"
        )

        votes = {}
        errors = []
        coordinator_id = f"p2p-coordinator-{voting_round_id}"

        # Subscribe to votes
        vote_queue = await self.broker.subscribe(
            coordinator_id,
            message_types=[MessageType.RESPONSE, MessageType.ERROR],
        )

        try:
            # Send proposal to all peers
            for peer_id in self.peer_ids:
                message = A2AMessage(
                    conversation_id=voting_round_id,
                    from_agent_id=coordinator_id,
                    to_agent_id=peer_id,
                    message_type=MessageType.REQUEST,
                    payload={"proposal": proposal, "voting_round": voting_round_id},
                    requires_response=True,
                )
                await self.broker.publish(message)
                logger.debug(f"Sent proposal to peer {peer_id}")

            # Collect votes
            pending_peers = set(self.peer_ids)
            start_time = asyncio.get_event_loop().time()

            while pending_peers and (asyncio.get_event_loop().time() - start_time) < timeout:
                try:
                    remaining_timeout = timeout - (asyncio.get_event_loop().time() - start_time)
                    message = await asyncio.wait_for(
                        vote_queue.get(),
                        timeout=max(0.1, remaining_timeout),
                    )

                    if message.conversation_id != voting_round_id:
                        continue

                    peer_id = message.from_agent_id

                    if message.message_type == MessageType.RESPONSE:
                        vote = message.payload.get("vote")
                        votes[peer_id] = vote
                        pending_peers.discard(peer_id)
                        logger.debug(f"Received vote from peer {peer_id}: {vote}")

                    elif message.message_type == MessageType.ERROR:
                        error_msg = f"Peer {peer_id} error: {message.payload.get('error')}"
                        errors.append(error_msg)
                        pending_peers.discard(peer_id)
                        logger.warning(error_msg)

                except asyncio.TimeoutError:
                    break

            # Check for timeout
            if pending_peers:
                timeout_msg = f"Peers timed out: {pending_peers}"
                errors.append(timeout_msg)
                logger.warning(timeout_msg)

            # Calculate consensus
            total_votes = len(votes)
            positive_votes = sum(1 for vote in votes.values() if vote)
            negative_votes = total_votes - positive_votes
            consensus_reached = (positive_votes / len(self.peer_ids)) >= self.consensus_threshold

            success = total_votes > 0

            return OrchestrationResult(
                success=success,
                results={
                    "consensus_reached": consensus_reached,
                    "votes": votes,
                    "positive_votes": positive_votes,
                    "negative_votes": negative_votes,
                    "total_votes": total_votes,
                    "total_peers": len(self.peer_ids),
                    "consensus_threshold": self.consensus_threshold,
                },
                errors=errors,
                metadata={
                    "pattern": "peer_to_peer",
                    "voting_round_id": voting_round_id,
                    "peer_ids": self.peer_ids,
                },
            )

        finally:
            await self.broker.unsubscribe(coordinator_id)
