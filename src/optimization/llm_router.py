"""LLM Router for intelligent model selection based on task complexity.

This module provides the LLMRouter class which analyzes request complexity
and routes to the most cost-effective model while maintaining quality.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Optional, List
import re


class ComplexityLevel(Enum):
    """Task complexity levels for routing decisions."""

    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXPERT = "expert"


@dataclass
class ModelConfig:
    """Configuration for a language model."""

    model_name: str
    cost_per_1k_tokens: float
    max_tokens: int
    temperature: float = 0.7
    supports_functions: bool = False
    estimated_quality: float = 0.8  # 0.0 to 1.0


class LLMRouter:
    """Routes LLM requests to appropriate models based on complexity analysis.

    The router analyzes request characteristics to determine complexity level
    and selects the most cost-effective model that meets quality requirements.
    """

    def __init__(self) -> None:
        """Initialize the LLM router with default model configurations."""
        self._model_configs: Dict[ComplexityLevel, ModelConfig] = {
            ComplexityLevel.SIMPLE: ModelConfig(
                model_name="local-slm",
                cost_per_1k_tokens=0.0,
                max_tokens=2048,
                temperature=0.5,
                supports_functions=False,
                estimated_quality=0.7
            ),
            ComplexityLevel.MODERATE: ModelConfig(
                model_name="gpt-3.5-turbo",
                cost_per_1k_tokens=0.002,
                max_tokens=4096,
                temperature=0.7,
                supports_functions=True,
                estimated_quality=0.85
            ),
            ComplexityLevel.COMPLEX: ModelConfig(
                model_name="gpt-4",
                cost_per_1k_tokens=0.03,
                max_tokens=8192,
                temperature=0.7,
                supports_functions=True,
                estimated_quality=0.95
            ),
            ComplexityLevel.EXPERT: ModelConfig(
                model_name="gpt-4-turbo",
                cost_per_1k_tokens=0.01,
                max_tokens=128000,
                temperature=0.8,
                supports_functions=True,
                estimated_quality=0.98
            )
        }

        # Complexity indicators
        self._complexity_keywords = {
            ComplexityLevel.EXPERT: [
                "analyze", "evaluate", "design", "architect", "optimize",
                "refactor", "debug complex", "comprehensive", "strategic"
            ],
            ComplexityLevel.COMPLEX: [
                "explain", "compare", "generate code", "review", "implement",
                "integrate", "troubleshoot", "research"
            ],
            ComplexityLevel.MODERATE: [
                "summarize", "translate", "format", "convert", "list",
                "describe", "simple code", "basic"
            ]
        }

    def estimate_complexity(
        self,
        prompt: str,
        context_length: int = 0,
        requires_code: bool = False,
        requires_reasoning: bool = False,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ComplexityLevel:
        """Estimate the complexity level of a request.

        Args:
            prompt: The user's request text
            context_length: Length of conversation context in tokens
            requires_code: Whether the task requires code generation
            requires_reasoning: Whether the task requires multi-step reasoning
            metadata: Additional metadata for complexity estimation

        Returns:
            ComplexityLevel enum indicating the estimated complexity
        """
        metadata = metadata or {}
        score = 0

        # Analyze prompt length
        prompt_length = len(prompt.split())
        if prompt_length > 200:
            score += 3
        elif prompt_length > 100:
            score += 2
        elif prompt_length > 50:
            score += 1

        # Analyze context length
        if context_length > 10000:
            score += 3
        elif context_length > 5000:
            score += 2
        elif context_length > 1000:
            score += 1

        # Check for complexity keywords
        prompt_lower = prompt.lower()
        for level, keywords in self._complexity_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                if level == ComplexityLevel.EXPERT:
                    score += 4
                elif level == ComplexityLevel.COMPLEX:
                    score += 2
                elif level == ComplexityLevel.MODERATE:
                    score += 1
                break

        # Code generation adds complexity
        if requires_code:
            score += 2

        # Multi-step reasoning adds complexity
        if requires_reasoning:
            score += 2

        # Check for function calling requirement
        if metadata.get("requires_functions", False):
            score += 2

        # Check for technical depth indicators
        technical_patterns = [
            r'\b(?:algorithm|complexity|performance|optimization)\b',
            r'\b(?:architecture|design pattern|best practice)\b',
            r'\b(?:security|authentication|authorization)\b',
            r'\b(?:distributed|concurrent|parallel|async)\b'
        ]

        for pattern in technical_patterns:
            if re.search(pattern, prompt_lower):
                score += 1

        # Map score to complexity level
        if score >= 10:
            return ComplexityLevel.EXPERT
        elif score >= 6:
            return ComplexityLevel.COMPLEX
        elif score >= 3:
            return ComplexityLevel.MODERATE
        else:
            return ComplexityLevel.SIMPLE

    def route(
        self,
        prompt: str,
        context_length: int = 0,
        requires_code: bool = False,
        requires_reasoning: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
        force_model: Optional[str] = None
    ) -> ModelConfig:
        """Route a request to the appropriate model.

        Args:
            prompt: The user's request text
            context_length: Length of conversation context in tokens
            requires_code: Whether the task requires code generation
            requires_reasoning: Whether the task requires multi-step reasoning
            metadata: Additional metadata for routing decisions
            force_model: Optional model name to force specific routing

        Returns:
            ModelConfig with the selected model configuration
        """
        # Check for forced model
        if force_model:
            for config in self._model_configs.values():
                if config.model_name == force_model:
                    return config

        # Estimate complexity
        complexity = self.estimate_complexity(
            prompt=prompt,
            context_length=context_length,
            requires_code=requires_code,
            requires_reasoning=requires_reasoning,
            metadata=metadata
        )

        # Get model configuration for complexity level
        model_config = self._model_configs[complexity]

        # Check if we need to upgrade based on context length
        if context_length > model_config.max_tokens:
            # Upgrade to model with larger context window
            for level in [ComplexityLevel.EXPERT, ComplexityLevel.COMPLEX,
                         ComplexityLevel.MODERATE, ComplexityLevel.SIMPLE]:
                config = self._model_configs[level]
                if config.max_tokens >= context_length:
                    model_config = config
                    break

        return model_config

    def add_model_config(
        self,
        complexity_level: ComplexityLevel,
        config: ModelConfig
    ) -> None:
        """Add or update a model configuration for a complexity level.

        Args:
            complexity_level: The complexity level to associate with this model
            config: The model configuration
        """
        self._model_configs[complexity_level] = config

    def get_model_config(
        self,
        complexity_level: ComplexityLevel
    ) -> Optional[ModelConfig]:
        """Get the model configuration for a complexity level.

        Args:
            complexity_level: The complexity level

        Returns:
            ModelConfig if found, None otherwise
        """
        return self._model_configs.get(complexity_level)

    def get_all_models(self) -> Dict[ComplexityLevel, ModelConfig]:
        """Get all model configurations.

        Returns:
            Dictionary mapping complexity levels to model configurations
        """
        return self._model_configs.copy()

    def estimate_cost(
        self,
        prompt: str,
        expected_response_tokens: int = 500,
        context_length: int = 0,
        requires_code: bool = False,
        requires_reasoning: bool = False,
        metadata: Optional[Dict[str, Any]] = None
    ) -> float:
        """Estimate the cost of a request.

        Args:
            prompt: The user's request text
            expected_response_tokens: Expected length of response
            context_length: Length of conversation context in tokens
            requires_code: Whether the task requires code generation
            requires_reasoning: Whether the task requires multi-step reasoning
            metadata: Additional metadata for cost estimation

        Returns:
            Estimated cost in dollars
        """
        model_config = self.route(
            prompt=prompt,
            context_length=context_length,
            requires_code=requires_code,
            requires_reasoning=requires_reasoning,
            metadata=metadata
        )

        # Estimate total tokens (rough approximation: 1 word ≈ 1.3 tokens)
        prompt_tokens = len(prompt.split()) * 1.3 + context_length
        total_tokens = prompt_tokens + expected_response_tokens

        # Calculate cost
        cost = (total_tokens / 1000) * model_config.cost_per_1k_tokens

        return cost
