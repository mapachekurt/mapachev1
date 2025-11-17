"""Message Broker for Agent-to-Agent Communication.

This module provides an in-memory message broker implementation for publish/subscribe
messaging patterns between agents.
"""

import asyncio
from collections import defaultdict
from typing import Callable, Dict, List, Optional, Set
import logging

from .a2a_protocol import A2AMessage, MessageType


logger = logging.getLogger(__name__)


class MessageBroker:
    """In-memory message broker for agent communication.

    Provides publish/subscribe functionality for A2A messages with support for:
    - Topic-based subscriptions
    - Agent-specific subscriptions
    - Message type filtering
    - Message persistence (optional, in-memory)
    - Dead letter queue for failed messages
    """

    def __init__(self, max_queue_size: int = 1000, enable_persistence: bool = False):
        """Initialize the message broker.

        Args:
            max_queue_size: Maximum number of messages to queue per subscriber
            enable_persistence: Whether to keep a history of all messages
        """
        self._subscribers: Dict[str, Set[asyncio.Queue]] = defaultdict(set)
        self._agent_subscribers: Dict[str, asyncio.Queue] = {}
        self._type_subscribers: Dict[MessageType, Set[asyncio.Queue]] = defaultdict(set)
        self._max_queue_size = max_queue_size
        self._enable_persistence = enable_persistence
        self._message_history: List[A2AMessage] = [] if enable_persistence else None
        self._dead_letter_queue: List[A2AMessage] = []
        self._lock = asyncio.Lock()
        self._running = True

        logger.info(
            f"MessageBroker initialized (max_queue_size={max_queue_size}, "
            f"persistence={enable_persistence})"
        )

    async def publish(
        self,
        message: A2AMessage,
        topic: Optional[str] = None,
    ) -> bool:
        """Publish a message to subscribers.

        Args:
            message: The A2A message to publish
            topic: Optional topic to publish to (in addition to agent/type routing)

        Returns:
            True if message was delivered to at least one subscriber, False otherwise
        """
        async with self._lock:
            if not self._running:
                logger.warning("MessageBroker is not running, message rejected")
                return False

            # Store in history if persistence is enabled
            if self._enable_persistence:
                self._message_history.append(message)

            delivered = False
            delivery_queues: Set[asyncio.Queue] = set()

            # Collect all queues that should receive this message
            # 1. Topic subscribers
            if topic and topic in self._subscribers:
                delivery_queues.update(self._subscribers[topic])

            # 2. Agent-specific subscription
            if message.to_agent_id and message.to_agent_id in self._agent_subscribers:
                delivery_queues.add(self._agent_subscribers[message.to_agent_id])

            # 3. Message type subscribers
            if message.message_type in self._type_subscribers:
                delivery_queues.update(self._type_subscribers[message.message_type])

            # 4. Broadcast (no specific recipient)
            if not message.to_agent_id and "broadcast" in self._subscribers:
                delivery_queues.update(self._subscribers["broadcast"])

            # Deliver to all queues
            for queue in delivery_queues:
                try:
                    if queue.qsize() < self._max_queue_size:
                        queue.put_nowait(message)
                        delivered = True
                    else:
                        logger.warning(
                            f"Queue full, moving message {message.message_id} to dead letter queue"
                        )
                        self._dead_letter_queue.append(message)
                except asyncio.QueueFull:
                    logger.warning(
                        f"Queue full, moving message {message.message_id} to dead letter queue"
                    )
                    self._dead_letter_queue.append(message)

            if delivered:
                logger.debug(
                    f"Published message {message.message_id} from {message.from_agent_id} "
                    f"to {len(delivery_queues)} subscriber(s)"
                )
            else:
                logger.warning(
                    f"Message {message.message_id} has no subscribers, "
                    f"moved to dead letter queue"
                )
                self._dead_letter_queue.append(message)

            return delivered

    async def subscribe(
        self,
        agent_id: str,
        topic: Optional[str] = None,
        message_types: Optional[List[MessageType]] = None,
    ) -> asyncio.Queue:
        """Subscribe to messages.

        Args:
            agent_id: ID of the subscribing agent
            topic: Optional topic to subscribe to
            message_types: Optional list of message types to subscribe to

        Returns:
            Queue that will receive matching messages
        """
        async with self._lock:
            # Create a new queue for this subscription
            queue = asyncio.Queue(maxsize=self._max_queue_size)

            # Subscribe to agent-specific messages
            self._agent_subscribers[agent_id] = queue

            # Subscribe to topic if provided
            if topic:
                self._subscribers[topic].add(queue)
                logger.debug(f"Agent {agent_id} subscribed to topic '{topic}'")

            # Subscribe to message types if provided
            if message_types:
                for msg_type in message_types:
                    self._type_subscribers[msg_type].add(queue)
                logger.debug(
                    f"Agent {agent_id} subscribed to message types: "
                    f"{[mt.value for mt in message_types]}"
                )

            logger.info(f"Agent {agent_id} subscribed to message broker")
            return queue

    async def unsubscribe(self, agent_id: str) -> None:
        """Unsubscribe an agent from all messages.

        Args:
            agent_id: ID of the agent to unsubscribe
        """
        async with self._lock:
            # Remove from agent subscribers
            queue = self._agent_subscribers.pop(agent_id, None)

            if queue:
                # Remove from topic subscribers
                for topic_queues in self._subscribers.values():
                    topic_queues.discard(queue)

                # Remove from type subscribers
                for type_queues in self._type_subscribers.values():
                    type_queues.discard(queue)

                logger.info(f"Agent {agent_id} unsubscribed from message broker")

    async def get_message_history(
        self,
        agent_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        message_type: Optional[MessageType] = None,
        limit: int = 100,
    ) -> List[A2AMessage]:
        """Retrieve message history (if persistence is enabled).

        Args:
            agent_id: Filter by agent ID (sender or receiver)
            conversation_id: Filter by conversation ID
            message_type: Filter by message type
            limit: Maximum number of messages to return

        Returns:
            List of matching messages
        """
        if not self._enable_persistence:
            logger.warning("Message persistence is not enabled")
            return []

        async with self._lock:
            messages = self._message_history

            # Apply filters
            if agent_id:
                messages = [
                    m for m in messages
                    if m.from_agent_id == agent_id or m.to_agent_id == agent_id
                ]

            if conversation_id:
                messages = [m for m in messages if m.conversation_id == conversation_id]

            if message_type:
                messages = [m for m in messages if m.message_type == message_type]

            # Return most recent messages up to limit
            return messages[-limit:]

    async def get_dead_letter_messages(self, limit: int = 100) -> List[A2AMessage]:
        """Retrieve messages from the dead letter queue.

        Args:
            limit: Maximum number of messages to return

        Returns:
            List of dead letter messages
        """
        async with self._lock:
            return self._dead_letter_queue[-limit:]

    async def clear_dead_letter_queue(self) -> int:
        """Clear the dead letter queue.

        Returns:
            Number of messages cleared
        """
        async with self._lock:
            count = len(self._dead_letter_queue)
            self._dead_letter_queue.clear()
            logger.info(f"Cleared {count} messages from dead letter queue")
            return count

    async def shutdown(self) -> None:
        """Shutdown the message broker."""
        async with self._lock:
            self._running = False
            self._subscribers.clear()
            self._agent_subscribers.clear()
            self._type_subscribers.clear()
            logger.info("MessageBroker shut down")

    def get_stats(self) -> Dict[str, int]:
        """Get broker statistics.

        Returns:
            Dictionary with broker statistics
        """
        return {
            "total_subscribers": len(self._agent_subscribers),
            "topic_subscriptions": sum(len(queues) for queues in self._subscribers.values()),
            "type_subscriptions": sum(len(queues) for queues in self._type_subscribers.values()),
            "messages_in_history": len(self._message_history) if self._enable_persistence else 0,
            "dead_letter_count": len(self._dead_letter_queue),
        }
