"""Vector Memory - Long-term memory storage with vector search.

This module provides long-term memory capabilities using in-memory vector
storage with cosine similarity search. Designed to work without external
dependencies like vector databases.
"""

import hashlib
import json
import math
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4


@dataclass
class MemoryVector:
    """A memory entry with vector embedding.

    Attributes:
        memory_id: Unique identifier for this memory
        agent_id: ID of the agent owning this memory
        content: Text content of the memory
        embedding: Vector embedding of the content
        timestamp: When this memory was created
        access_count: Number of times this memory was accessed
        last_accessed: When this memory was last accessed
        importance: Importance score (0.0 to 1.0)
        metadata: Additional metadata for the memory
        tags: List of tags for categorization
    """

    memory_id: str = field(default_factory=lambda: str(uuid4()))
    agent_id: str = ""
    content: str = ""
    embedding: List[float] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.utcnow)
    importance: float = 0.5
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert memory to dictionary representation.

        Returns:
            Dictionary containing all memory fields
        """
        return {
            "memory_id": self.memory_id,
            "agent_id": self.agent_id,
            "content": self.content,
            "embedding": self.embedding,
            "timestamp": self.timestamp.isoformat(),
            "access_count": self.access_count,
            "last_accessed": self.last_accessed.isoformat(),
            "importance": self.importance,
            "metadata": self.metadata,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryVector":
        """Create memory from dictionary representation.

        Args:
            data: Dictionary containing memory fields

        Returns:
            MemoryVector instance
        """
        return cls(
            memory_id=data.get("memory_id", str(uuid4())),
            agent_id=data.get("agent_id", ""),
            content=data.get("content", ""),
            embedding=data.get("embedding", []),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.utcnow(),
            access_count=data.get("access_count", 0),
            last_accessed=datetime.fromisoformat(data["last_accessed"]) if "last_accessed" in data else datetime.utcnow(),
            importance=data.get("importance", 0.5),
            metadata=data.get("metadata", {}),
            tags=data.get("tags", []),
        )


@dataclass
class SearchResult:
    """Result from vector similarity search.

    Attributes:
        memory: The memory entry
        similarity: Cosine similarity score (0.0 to 1.0)
        rank: Rank in search results (0-based)
    """

    memory: MemoryVector
    similarity: float
    rank: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert search result to dictionary.

        Returns:
            Dictionary containing result fields
        """
        return {
            "memory": self.memory.to_dict(),
            "similarity": self.similarity,
            "rank": self.rank,
        }


class SimpleEmbedding:
    """
    Simple embedding generator for text without external dependencies.

    Uses a combination of character-based and word-based features to
    create deterministic embeddings. Not as sophisticated as transformer
    models but works without external dependencies.
    """

    def __init__(self, embedding_dim: int = 128):
        """
        Initialize embedding generator.

        Args:
            embedding_dim: Dimension of the embedding vectors
        """
        self.embedding_dim = embedding_dim

    def embed(self, text: str) -> List[float]:
        """
        Generate embedding for text.

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding vector
        """
        if not text:
            return [0.0] * self.embedding_dim

        # Normalize text
        text = text.lower().strip()

        # Create a hash-based seed for deterministic embeddings
        text_hash = hashlib.md5(text.encode()).hexdigest()

        # Extract features
        words = text.split()
        word_count = len(words)
        char_count = len(text)
        avg_word_length = char_count / word_count if word_count > 0 else 0

        # Create embedding vector
        embedding = []

        # Feature 1: Character distribution (first 32 dims)
        char_counts = {}
        for char in text:
            char_counts[char] = char_counts.get(char, 0) + 1

        for i in range(32):
            char_code = ord('a') + i if i < 26 else ord('0') + (i - 26)
            char = chr(char_code)
            count = char_counts.get(char, 0)
            normalized = count / char_count if char_count > 0 else 0
            embedding.append(normalized)

        # Feature 2: Word-based features (next 32 dims)
        word_hashes = [hashlib.md5(word.encode()).digest() for word in words[:32]]
        for i in range(32):
            if i < len(word_hashes):
                # Use first byte of hash, normalized
                val = word_hashes[i][0] / 255.0
            else:
                val = 0.0
            embedding.append(val)

        # Feature 3: Statistical features (next 32 dims)
        for i in range(32):
            # Use different parts of the text hash
            hash_byte = int(text_hash[i * 2:(i * 2) + 2], 16) if i < len(text_hash) // 2 else 0
            normalized = hash_byte / 255.0
            embedding.append(normalized)

        # Feature 4: Structural features (remaining dims)
        remaining = self.embedding_dim - len(embedding)
        for i in range(remaining):
            # Combine various text statistics
            if i == 0:
                val = min(word_count / 100.0, 1.0)  # Word count feature
            elif i == 1:
                val = min(char_count / 500.0, 1.0)  # Char count feature
            elif i == 2:
                val = min(avg_word_length / 10.0, 1.0)  # Avg word length
            else:
                # Use hash for remaining dimensions
                hash_idx = i % len(text_hash)
                val = int(text_hash[hash_idx], 16) / 15.0
            embedding.append(val)

        # Normalize the embedding vector
        magnitude = math.sqrt(sum(x * x for x in embedding))
        if magnitude > 0:
            embedding = [x / magnitude for x in embedding]

        return embedding


class VectorMemory:
    """
    Long-term memory storage with vector similarity search.

    Provides semantic search capabilities over stored memories using
    cosine similarity. Works entirely in-memory without external
    vector database dependencies.
    """

    def __init__(
        self,
        embedding_dim: int = 128,
        embedder: Optional[SimpleEmbedding] = None,
    ):
        """
        Initialize vector memory.

        Args:
            embedding_dim: Dimension of embedding vectors
            embedder: Optional custom embedding generator
        """
        self.embedding_dim = embedding_dim
        self.embedder = embedder or SimpleEmbedding(embedding_dim)
        self.memories: Dict[str, MemoryVector] = {}

    def store(
        self,
        agent_id: str,
        content: str,
        importance: float = 0.5,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ) -> str:
        """
        Store a new memory.

        Args:
            agent_id: ID of the agent storing the memory
            content: Text content of the memory
            importance: Importance score (0.0 to 1.0)
            tags: Optional list of tags
            metadata: Optional metadata dictionary
            embedding: Optional pre-computed embedding (will generate if None)

        Returns:
            memory_id: ID of the stored memory
        """
        # Generate embedding if not provided
        if embedding is None:
            embedding = self.embedder.embed(content)

        memory = MemoryVector(
            agent_id=agent_id,
            content=content,
            embedding=embedding,
            importance=importance,
            tags=tags or [],
            metadata=metadata or {},
        )

        self.memories[memory.memory_id] = memory
        return memory.memory_id

    def get(self, memory_id: str) -> Optional[MemoryVector]:
        """
        Retrieve a memory by ID.

        Args:
            memory_id: ID of the memory to retrieve

        Returns:
            MemoryVector or None if not found
        """
        memory = self.memories.get(memory_id)
        if memory:
            memory.access_count += 1
            memory.last_accessed = datetime.utcnow()
        return memory

    def delete(self, memory_id: str) -> bool:
        """
        Delete a memory.

        Args:
            memory_id: ID of the memory to delete

        Returns:
            True if deleted, False if not found
        """
        if memory_id in self.memories:
            del self.memories[memory_id]
            return True
        return False

    def search(
        self,
        query: str,
        agent_id: Optional[str] = None,
        top_k: int = 10,
        min_similarity: float = 0.0,
        tags: Optional[List[str]] = None,
        query_embedding: Optional[List[float]] = None,
    ) -> List[SearchResult]:
        """
        Search for similar memories using cosine similarity.

        Args:
            query: Query text to search for
            agent_id: Optional agent ID to filter by
            top_k: Number of top results to return
            min_similarity: Minimum similarity threshold (0.0 to 1.0)
            tags: Optional list of tags to filter by
            query_embedding: Optional pre-computed query embedding

        Returns:
            List of SearchResult objects ordered by similarity
        """
        # Generate query embedding if not provided
        if query_embedding is None:
            query_embedding = self.embedder.embed(query)

        # Filter memories
        candidate_memories = []
        for memory in self.memories.values():
            # Filter by agent_id if specified
            if agent_id and memory.agent_id != agent_id:
                continue

            # Filter by tags if specified
            if tags and not any(tag in memory.tags for tag in tags):
                continue

            candidate_memories.append(memory)

        # Calculate similarities
        results = []
        for memory in candidate_memories:
            similarity = self._cosine_similarity(query_embedding, memory.embedding)

            if similarity >= min_similarity:
                results.append((memory, similarity))

                # Update access statistics
                memory.access_count += 1
                memory.last_accessed = datetime.utcnow()

        # Sort by similarity (descending)
        results.sort(key=lambda x: x[1], reverse=True)

        # Take top_k results
        results = results[:top_k]

        # Create SearchResult objects
        search_results = [
            SearchResult(memory=memory, similarity=similarity, rank=i)
            for i, (memory, similarity) in enumerate(results)
        ]

        return search_results

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Cosine similarity score (0.0 to 1.0)
        """
        if len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        similarity = dot_product / (magnitude1 * magnitude2)

        # Normalize to 0-1 range (cosine can be -1 to 1)
        return max(0.0, min(1.0, (similarity + 1.0) / 2.0))

    def get_memories_by_agent(self, agent_id: str) -> List[MemoryVector]:
        """
        Get all memories for a specific agent.

        Args:
            agent_id: ID of the agent

        Returns:
            List of memories belonging to the agent
        """
        return [
            memory for memory in self.memories.values()
            if memory.agent_id == agent_id
        ]

    def get_memories_by_tags(self, tags: List[str]) -> List[MemoryVector]:
        """
        Get all memories with any of the specified tags.

        Args:
            tags: List of tags to search for

        Returns:
            List of memories with matching tags
        """
        return [
            memory for memory in self.memories.values()
            if any(tag in memory.tags for tag in tags)
        ]

    def update_importance(self, memory_id: str, importance: float) -> bool:
        """
        Update the importance score of a memory.

        Args:
            memory_id: ID of the memory
            importance: New importance score (0.0 to 1.0)

        Returns:
            True if updated, False if not found
        """
        memory = self.memories.get(memory_id)
        if memory:
            memory.importance = max(0.0, min(1.0, importance))
            return True
        return False

    def get_memory_count(self) -> int:
        """
        Get the total number of stored memories.

        Returns:
            Number of memories in storage
        """
        return len(self.memories)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about stored memories.

        Returns:
            Dictionary containing memory statistics
        """
        if not self.memories:
            return {
                "total_memories": 0,
                "avg_importance": 0.0,
                "avg_access_count": 0.0,
                "total_agents": 0,
                "total_tags": 0,
            }

        total_importance = sum(m.importance for m in self.memories.values())
        total_access_count = sum(m.access_count for m in self.memories.values())
        unique_agents = set(m.agent_id for m in self.memories.values())
        all_tags = set()
        for m in self.memories.values():
            all_tags.update(m.tags)

        return {
            "total_memories": len(self.memories),
            "avg_importance": total_importance / len(self.memories),
            "avg_access_count": total_access_count / len(self.memories),
            "total_agents": len(unique_agents),
            "total_tags": len(all_tags),
        }

    def export_memories(self) -> List[Dict[str, Any]]:
        """
        Export all memories to a list of dictionaries.

        Returns:
            List of memory dictionaries
        """
        return [memory.to_dict() for memory in self.memories.values()]

    def import_memories(self, memories_data: List[Dict[str, Any]]) -> int:
        """
        Import memories from a list of dictionaries.

        Args:
            memories_data: List of memory dictionaries

        Returns:
            Number of memories imported
        """
        count = 0
        for data in memories_data:
            try:
                memory = MemoryVector.from_dict(data)
                self.memories[memory.memory_id] = memory
                count += 1
            except (KeyError, ValueError):
                continue

        return count
