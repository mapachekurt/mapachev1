"""
Comprehensive tests for context engineering.

All tests use mocks - no cloud resources required.
"""

import pytest
from datetime import datetime
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from context.session_manager import Session, SessionEvent, SessionManager
from context.memory_types import ContextMemorySystem, DeclarativeMemory, ProceduralMemory
from context.memory_extraction import MemoryExtractor
from context.provenance import MemoryProvenance, ProvenanceMemory
from context.orchestrator import ContextOrchestrator


class TestSessionManager:
    """Test session lifecycle."""

    def test_create_session(self):
        """Test session creation."""
        session = Session(
            user_id="kurt",
            agent_id="financial_analyst",
            task_type="analysis"
        )

        assert session.user_id == "kurt"
        assert session.agent_id == "financial_analyst"
        assert session.task_type == "analysis"
        assert session.status == "active"

    def test_add_events(self):
        """Test adding events to session."""
        session = Session("kurt", "test_agent", "test")

        session.add_user_message("Hello")
        session.add_agent_response("Hi there!")

        assert len(session.state.conversation_history) == 2
        assert session.state.conversation_history[0].event_type == "user_message"
        assert session.state.conversation_history[1].event_type == "agent_response"

    def test_close_session(self):
        """Test session closure."""
        session = Session("kurt", "test_agent", "test")
        session.add_user_message("Test message")

        summary = session.close()

        assert session.status == "closed"
        assert summary["events_count"] == 1
        assert "duration_seconds" in summary

    def test_intent_extraction(self):
        """Test intent extraction from messages."""
        session = Session("kurt", "test_agent", "test")

        session.add_user_message("Analyze the revenue trends")
        assert "analysis" in session.state.extracted_intents

        session.add_user_message("Debug this error")
        assert "debugging" in session.state.extracted_intents

        session.add_user_message("Create a new feature")
        assert "creation" in session.state.extracted_intents

    def test_session_manager(self):
        """Test session manager functionality."""
        manager = SessionManager()

        # Create session
        session = manager.create_session("kurt", "test_agent", "analysis")
        assert session.session_id in manager.active_sessions

        # Get session
        retrieved = manager.get_session(session.session_id)
        assert retrieved.user_id == "kurt"

        # Close session
        summary = manager.close_session(session.session_id)
        assert session.session_id not in manager.active_sessions
        assert len(manager.session_history) == 1


class TestMemoryTypes:
    """Test declarative and procedural memory."""

    def test_declarative_memory(self):
        """Test storing and retrieving facts."""
        memory = DeclarativeMemory()

        memory.store_fact("preferred_language", "Python", confidence=1.0)
        memory.store_fact("timezone", "Europe/Berlin", confidence=0.9)

        assert memory.get_fact("preferred_language") == "Python"
        assert memory.get_fact("timezone") == "Europe/Berlin"
        assert len(memory.get_all_facts()) == 2

    def test_declarative_update(self):
        """Test updating facts with confidence."""
        memory = DeclarativeMemory()

        memory.store_fact("company_size", "small", confidence=0.6)
        memory.update_fact("company_size", "large", confidence=0.9)

        # Higher confidence should win
        assert memory.get_fact("company_size") == "large"

    def test_declarative_confidence_filtering(self):
        """Test filtering facts by confidence."""
        memory = DeclarativeMemory()

        memory.store_fact("high_confidence", "value1", confidence=0.9)
        memory.store_fact("low_confidence", "value2", confidence=0.3)

        facts = memory.get_all_facts(min_confidence=0.5)
        assert "high_confidence" in facts
        assert "low_confidence" not in facts

    def test_declarative_search(self):
        """Test searching facts."""
        memory = DeclarativeMemory()

        memory.store_fact("python_preference", "strongly prefer Python", confidence=1.0)
        memory.store_fact("java_opinion", "rarely use Java", confidence=0.8)

        results = memory.search_facts("python")
        assert len(results) == 1
        assert results[0]["key"] == "python_preference"

    def test_procedural_memory(self):
        """Test storing and retrieving patterns."""
        memory = ProceduralMemory()

        pattern_id = memory.store_pattern(
            pattern_type="debugging",
            description="Check logs before code",
            examples=["Session 1", "Session 3"],
            confidence=0.9
        )

        patterns = memory.get_patterns("debugging")
        assert len(patterns) == 1
        assert patterns[0]["description"] == "Check logs before code"

    def test_procedural_update(self):
        """Test updating patterns."""
        memory = ProceduralMemory()

        pattern_id = memory.store_pattern(
            "debugging", "Logs first approach", [], 0.7
        )

        memory.update_pattern(pattern_id, new_examples=["Session 5"], confidence_delta=0.1)

        patterns = memory.get_patterns("debugging")
        assert patterns[0]["confidence"] == 0.8
        assert "Session 5" in patterns[0]["examples"]
        assert patterns[0]["usage_count"] == 1

    def test_procedural_search_relevant(self):
        """Test searching relevant patterns."""
        memory = ProceduralMemory()

        memory.store_pattern(
            "debugging", "Check logs before code", [], 0.9
        )
        memory.store_pattern(
            "planning", "Start with specs", [], 0.8
        )

        relevant = memory.search_relevant_patterns("debugging an error", limit=5)
        assert len(relevant) >= 1
        assert relevant[0]["type"] == "debugging"

    def test_context_memory_system(self):
        """Test combined memory system."""
        system = ContextMemorySystem("kurt")

        # Add declarative fact
        system.declarative.store_fact("name", "Kurt", confidence=1.0)

        # Add procedural pattern
        system.procedural.store_pattern(
            "planning", "Start with comprehensive specs", [], 0.9
        )

        # Get proactive context
        context = system.get_proactive_context()
        assert "declarative_facts" in context
        assert "key_patterns" in context

    def test_context_memory_reactive(self):
        """Test reactive context retrieval."""
        system = ContextMemorySystem("kurt")

        system.declarative.store_fact("python_preference", "Python expert", confidence=0.9)
        system.procedural.store_pattern(
            "debugging", "Logs first", [], 0.8
        )

        reactive = system.get_reactive_context("debugging a Python error")
        assert "relevant_patterns" in reactive
        assert "task_specific_facts" in reactive

    def test_context_memory_token_budget(self):
        """Test token budget management."""
        system = ContextMemorySystem("kurt")

        # Add lots of data
        for i in range(20):
            system.declarative.store_fact(f"fact_{i}", f"value_{i}", confidence=0.8)
            system.procedural.store_pattern(
                f"type_{i}", f"description_{i}", [], 0.8
            )

        # Get full context with token limit
        context = system.get_full_context("test task", max_tokens=100)
        assert "proactive" in context
        assert "reactive" in context


class TestMemoryExtraction:
    """Test LLM-driven memory extraction."""

    @pytest.mark.asyncio
    async def test_extract_from_session(self):
        """Test extracting memories from session."""
        session = Session("kurt", "test_agent", "analysis")
        session.add_user_message("I prefer Python over JavaScript")
        session.add_agent_response("Noted, I'll remember that")
        session.close()

        extractor = MemoryExtractor()
        memories = await extractor.extract_from_session(session, MockLLM())

        assert "declarative" in memories
        assert "procedural" in memories

    @pytest.mark.asyncio
    async def test_consolidate_memories(self):
        """Test memory consolidation."""
        system = ContextMemorySystem("kurt")
        extractor = MemoryExtractor()

        new_memories = {
            "declarative": [
                {"key": "language", "value": "Python", "confidence": 0.9}
            ],
            "procedural": []
        }

        stats = await extractor.consolidate_memories(
            new_memories,
            system,
            "session-123"
        )

        assert stats["declarative_added"] == 1
        assert system.declarative.get_fact("language") == "Python"

    @pytest.mark.asyncio
    async def test_consolidate_update_existing(self):
        """Test consolidating with existing memories."""
        system = ContextMemorySystem("kurt")
        extractor = MemoryExtractor()

        # Add initial memory
        system.declarative.store_fact("language", "JavaScript", confidence=0.5)

        # Consolidate with higher confidence
        new_memories = {
            "declarative": [
                {"key": "language", "value": "Python", "confidence": 0.9}
            ],
            "procedural": []
        }

        stats = await extractor.consolidate_memories(
            new_memories,
            system,
            "session-123"
        )

        assert stats["declarative_updated"] == 1
        assert system.declarative.get_fact("language") == "Python"

    @pytest.mark.asyncio
    async def test_format_conversation(self):
        """Test conversation formatting."""
        session = Session("kurt", "test_agent", "test")
        session.add_user_message("Hello")
        session.add_agent_response("Hi")
        session.add_tool_call("calculator", "42")

        extractor = MemoryExtractor()
        formatted = extractor._format_conversation(session)

        assert "User: Hello" in formatted
        assert "Agent: Hi" in formatted
        assert "Tool: calculator" in formatted


class TestProvenance:
    """Test memory provenance tracking."""

    def test_provenance_creation(self):
        """Test creating provenance."""
        prov = MemoryProvenance(
            source_session_id="session-123",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            confidence=0.8,
            verification_count=1,
            contradiction_count=0
        )

        assert prov.confidence == 0.8
        assert prov.verification_count == 1

    def test_confidence_increase(self):
        """Test confidence increase."""
        prov = MemoryProvenance(
            source_session_id="session-123",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            confidence=0.5,
            verification_count=1,
            contradiction_count=0
        )

        prov.increase_confidence()
        assert prov.confidence == 0.6
        assert prov.verification_count == 2

    def test_confidence_decrease(self):
        """Test confidence decrease."""
        prov = MemoryProvenance(
            source_session_id="session-123",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            confidence=0.5,
            verification_count=1,
            contradiction_count=0
        )

        prov.decrease_confidence()
        assert prov.confidence == 0.3
        assert prov.contradiction_count == 1

    def test_confidence_bounds(self):
        """Test confidence stays within bounds."""
        prov = MemoryProvenance(
            source_session_id="session-123",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            confidence=0.95,
            verification_count=1,
            contradiction_count=0
        )

        # Should cap at 1.0
        prov.increase_confidence()
        assert prov.confidence == 1.0

        # Multiple decreases
        for _ in range(10):
            prov.decrease_confidence()

        # Should floor at 0.0
        assert prov.confidence == 0.0

    def test_debug_info(self):
        """Test debug info generation."""
        prov = MemoryProvenance(
            source_session_id="session-123",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            confidence=0.8,
            verification_count=5,
            contradiction_count=1
        )

        debug = prov.debug_info()
        assert "source" in debug
        assert "confidence" in debug
        assert "verifications" in debug
        assert debug["verifications"] == 5


class TestOrchestrator:
    """Test context assembly orchestration."""

    @pytest.mark.asyncio
    async def test_process_query(self):
        """Test full query processing."""
        system = ContextMemorySystem("kurt")
        extractor = MemoryExtractor()
        orchestrator = ContextOrchestrator(system, extractor)

        session = Session("kurt", "test_agent", "test")

        result = await orchestrator.process_query(
            user_id="kurt",
            agent_id="test_agent",
            query="Analyze revenue trends",
            session=session,
            llm=MockLLM()
        )

        assert "response" in result
        assert "intent" in result
        assert "duration_ms" in result
        assert result["intent"] == "analysis"

    @pytest.mark.asyncio
    async def test_intent_parsing(self):
        """Test intent parsing."""
        system = ContextMemorySystem("kurt")
        extractor = MemoryExtractor()
        orchestrator = ContextOrchestrator(system, extractor)

        assert orchestrator._parse_intent("analyze the data") == "analysis"
        assert orchestrator._parse_intent("debug this error") == "debugging"
        assert orchestrator._parse_intent("create a new feature") == "creation"
        assert orchestrator._parse_intent("explain how this works") == "information"

    @pytest.mark.asyncio
    async def test_context_assembly(self):
        """Test full context assembly."""
        system = ContextMemorySystem("kurt")
        system.declarative.store_fact("name", "Kurt", confidence=1.0)

        extractor = MemoryExtractor()
        orchestrator = ContextOrchestrator(system, extractor)

        session = Session("kurt", "test_agent", "test")
        session.add_user_message("Previous message")

        result = await orchestrator.process_query(
            user_id="kurt",
            agent_id="test_agent",
            query="New query",
            session=session,
            llm=MockLLM()
        )

        context = result["context_used"]
        assert "memories" in context
        assert "session_context" in context
        assert len(context["session_context"]["recent_history"]) >= 1


class MockLLM:
    """Mock LLM for testing."""

    async def generate(self, prompt: str) -> str:
        return '{"declarative": [], "procedural": []}'


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
