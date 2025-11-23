"""Result caching system for LLM responses.

This module provides the ResultCache class which caches LLM responses
to reduce costs by avoiding duplicate API calls for similar requests.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
import hashlib
import json
from collections import OrderedDict


@dataclass
class CacheEntry:
    """Entry in the result cache."""

    key: str
    result: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    ttl_seconds: Optional[int] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class CacheStats:
    """Statistics about cache performance."""

    total_requests: int
    cache_hits: int
    cache_misses: int
    hit_rate: float
    total_entries: int
    total_size_bytes: int
    evictions: int


class ResultCache:
    """Cache for LLM responses to reduce API calls and costs.

    This cache uses semantic hashing to identify similar requests and
    implements LRU eviction with TTL support for memory management.
    """

    def __init__(
        self,
        max_size: int = 1000,
        default_ttl_seconds: Optional[int] = 3600,
        similarity_threshold: float = 0.95
    ) -> None:
        """Initialize the result cache.

        Args:
            max_size: Maximum number of entries in cache
            default_ttl_seconds: Default time-to-live for entries (None = no expiry)
            similarity_threshold: Threshold for semantic similarity matching (0.0-1.0)
        """
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._max_size = max_size
        self._default_ttl_seconds = default_ttl_seconds
        self._similarity_threshold = similarity_threshold

        # Statistics tracking
        self._stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "evictions": 0
        }

    def generate_key(
        self,
        prompt: str,
        model: str = "default",
        parameters: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        use_semantic: bool = True
    ) -> str:
        """Generate a cache key for a request.

        Args:
            prompt: The user's request text
            model: Model identifier
            parameters: Model parameters (temperature, max_tokens, etc.)
            context: Additional context that affects the response
            use_semantic: Whether to use semantic hashing (ignores minor variations)

        Returns:
            Cache key as a hex string
        """
        parameters = parameters or {}
        context = context or {}

        if use_semantic:
            # Normalize prompt for semantic matching
            normalized_prompt = self._normalize_prompt(prompt)
            key_data = {
                "prompt": normalized_prompt,
                "model": model,
                "temperature": parameters.get("temperature", 0.7),
                "max_tokens": parameters.get("max_tokens", 1000)
            }
        else:
            # Exact matching
            key_data = {
                "prompt": prompt,
                "model": model,
                "parameters": parameters,
                "context": context
            }

        # Create deterministic hash
        key_string = json.dumps(key_data, sort_keys=True)
        cache_key = hashlib.sha256(key_string.encode()).hexdigest()

        return cache_key

    def get(
        self,
        key: str,
        update_access: bool = True
    ) -> Optional[Any]:
        """Retrieve a result from the cache.

        Args:
            key: Cache key
            update_access: Whether to update access time and count

        Returns:
            Cached result if found and valid, None otherwise
        """
        self._stats["total_requests"] += 1

        if key not in self._cache:
            self._stats["cache_misses"] += 1
            return None

        entry = self._cache[key]

        # Check if entry has expired
        if entry.ttl_seconds is not None:
            age = (datetime.now() - entry.created_at).total_seconds()
            if age > entry.ttl_seconds:
                # Entry expired, remove it
                del self._cache[key]
                self._stats["cache_misses"] += 1
                return None

        # Update access information
        if update_access:
            entry.last_accessed = datetime.now()
            entry.access_count += 1

            # Move to end (most recently used)
            self._cache.move_to_end(key)

        self._stats["cache_hits"] += 1
        return entry.result

    def set(
        self,
        key: str,
        result: Any,
        metadata: Optional[Dict[str, Any]] = None,
        ttl_seconds: Optional[int] = None,
        tags: Optional[List[str]] = None
    ) -> None:
        """Store a result in the cache.

        Args:
            key: Cache key
            result: Result to cache
            metadata: Optional metadata about the result
            ttl_seconds: Time-to-live in seconds (None uses default)
            tags: Optional tags for categorization
        """
        metadata = metadata or {}
        tags = tags or []

        # Use default TTL if not specified
        if ttl_seconds is None:
            ttl_seconds = self._default_ttl_seconds

        # Check if we need to evict entries
        if len(self._cache) >= self._max_size and key not in self._cache:
            self._evict_lru()

        # Create cache entry
        entry = CacheEntry(
            key=key,
            result=result,
            metadata=metadata,
            ttl_seconds=ttl_seconds,
            tags=tags
        )

        # Store in cache
        self._cache[key] = entry

        # Move to end (most recently used)
        self._cache.move_to_end(key)

    def invalidate(self, key: str) -> bool:
        """Invalidate a cache entry.

        Args:
            key: Cache key to invalidate

        Returns:
            True if entry was found and removed, False otherwise
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def invalidate_by_tag(self, tag: str) -> int:
        """Invalidate all cache entries with a specific tag.

        Args:
            tag: Tag to match

        Returns:
            Number of entries invalidated
        """
        keys_to_remove = [
            key for key, entry in self._cache.items()
            if tag in entry.tags
        ]

        for key in keys_to_remove:
            del self._cache[key]

        return len(keys_to_remove)

    def clear(self) -> None:
        """Clear all entries from the cache."""
        self._cache.clear()

    def get_stats(self) -> CacheStats:
        """Get cache statistics.

        Returns:
            CacheStats with performance metrics
        """
        total_requests = self._stats["total_requests"]
        cache_hits = self._stats["cache_hits"]
        hit_rate = (cache_hits / total_requests * 100) if total_requests > 0 else 0

        # Estimate cache size
        total_size = sum(
            len(json.dumps(entry.result).encode())
            for entry in self._cache.values()
        )

        return CacheStats(
            total_requests=total_requests,
            cache_hits=cache_hits,
            cache_misses=self._stats["cache_misses"],
            hit_rate=round(hit_rate, 2),
            total_entries=len(self._cache),
            total_size_bytes=total_size,
            evictions=self._stats["evictions"]
        )

    def get_entry(self, key: str) -> Optional[CacheEntry]:
        """Get the full cache entry for a key.

        Args:
            key: Cache key

        Returns:
            CacheEntry if found, None otherwise
        """
        return self._cache.get(key)

    def search_by_metadata(
        self,
        metadata_filter: Dict[str, Any]
    ) -> List[Tuple[str, CacheEntry]]:
        """Search cache entries by metadata.

        Args:
            metadata_filter: Dictionary of metadata key-value pairs to match

        Returns:
            List of (key, entry) tuples matching the filter
        """
        results = []

        for key, entry in self._cache.items():
            # Check if all filter criteria match
            if all(
                entry.metadata.get(k) == v
                for k, v in metadata_filter.items()
            ):
                results.append((key, entry))

        return results

    def get_popular_entries(self, limit: int = 10) -> List[Tuple[str, CacheEntry]]:
        """Get the most frequently accessed cache entries.

        Args:
            limit: Maximum number of entries to return

        Returns:
            List of (key, entry) tuples sorted by access count
        """
        sorted_entries = sorted(
            self._cache.items(),
            key=lambda x: x[1].access_count,
            reverse=True
        )

        return sorted_entries[:limit]

    def cleanup_expired(self) -> int:
        """Remove all expired entries from the cache.

        Returns:
            Number of entries removed
        """
        now = datetime.now()
        keys_to_remove = []

        for key, entry in self._cache.items():
            if entry.ttl_seconds is not None:
                age = (now - entry.created_at).total_seconds()
                if age > entry.ttl_seconds:
                    keys_to_remove.append(key)

        for key in keys_to_remove:
            del self._cache[key]

        return len(keys_to_remove)

    def _normalize_prompt(self, prompt: str) -> str:
        """Normalize a prompt for semantic matching.

        Args:
            prompt: Original prompt text

        Returns:
            Normalized prompt
        """
        # Convert to lowercase
        normalized = prompt.lower().strip()

        # Remove extra whitespace
        normalized = " ".join(normalized.split())

        # Remove common punctuation that doesn't affect meaning
        for char in ",.!?;:":
            normalized = normalized.replace(char, "")

        return normalized

    def _evict_lru(self) -> None:
        """Evict the least recently used entry."""
        if self._cache:
            # Remove first item (least recently used)
            self._cache.popitem(last=False)
            self._stats["evictions"] += 1

    def _calculate_similarity(self, prompt1: str, prompt2: str) -> float:
        """Calculate semantic similarity between two prompts.

        Args:
            prompt1: First prompt
            prompt2: Second prompt

        Returns:
            Similarity score between 0.0 and 1.0
        """
        # Simple word-based similarity (in production, use embeddings)
        words1 = set(self._normalize_prompt(prompt1).split())
        words2 = set(self._normalize_prompt(prompt2).split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union)

    def find_similar(
        self,
        prompt: str,
        model: str = "default",
        threshold: Optional[float] = None
    ) -> List[Tuple[str, CacheEntry, float]]:
        """Find cache entries similar to a given prompt.

        Args:
            prompt: Prompt to match against
            model: Model identifier
            threshold: Similarity threshold (uses instance default if None)

        Returns:
            List of (key, entry, similarity) tuples above threshold
        """
        threshold = threshold or self._similarity_threshold
        results = []

        for key, entry in self._cache.items():
            # Skip if model doesn't match
            if entry.metadata.get("model") != model:
                continue

            # Calculate similarity
            cached_prompt = entry.metadata.get("prompt", "")
            similarity = self._calculate_similarity(prompt, cached_prompt)

            if similarity >= threshold:
                results.append((key, entry, similarity))

        # Sort by similarity (highest first)
        results.sort(key=lambda x: x[2], reverse=True)

        return results

    def update_metadata(
        self,
        key: str,
        metadata: Dict[str, Any],
        merge: bool = True
    ) -> bool:
        """Update metadata for a cache entry.

        Args:
            key: Cache key
            metadata: New metadata
            merge: Whether to merge with existing metadata or replace

        Returns:
            True if entry was found and updated, False otherwise
        """
        if key not in self._cache:
            return False

        entry = self._cache[key]

        if merge:
            entry.metadata.update(metadata)
        else:
            entry.metadata = metadata

        return True
