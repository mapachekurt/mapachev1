"""
Output Validator - Validates agent outputs against acceptance criteria.

This module provides validation logic for different validation modes
and handles error categorization.
"""

from enum import Enum
from typing import Any, Callable, Dict, Optional
import re


class ErrorCategory(Enum):
    """Categories for validation errors."""

    TIMEOUT = "timeout"
    COST_EXCEEDED = "cost_exceeded"
    INCORRECT_OUTPUT = "incorrect_output"
    MISSING_OUTPUT = "missing_output"
    FORMAT_ERROR = "format_error"
    EXCEPTION = "exception"


class ValidationError(Exception):
    """Custom exception for validation errors."""

    def __init__(self, message: str, category: ErrorCategory):
        super().__init__(message)
        self.category = category


class OutputValidator:
    """
    Validator for agent outputs.

    Validates outputs against acceptance criteria using different modes.
    """

    def __init__(self):
        """Initialize validator."""
        self.custom_validators: Dict[str, Callable] = {}

    def register_custom_validator(
        self, name: str, validator_func: Callable[[Any, Any], bool]
    ) -> None:
        """
        Register a custom validator function.

        Args:
            name: Name of the custom validator
            validator_func: Function that takes (actual_value, expected_value) and returns bool
        """
        self.custom_validators[name] = validator_func

    def validate_criterion(
        self,
        criterion: Any,  # AcceptanceCriterion type (avoiding circular import)
        actual_value: Any,
        expected_value: Any,
    ) -> bool:
        """
        Validate actual value against criterion.

        Args:
            criterion: Acceptance criterion
            actual_value: Actual value from agent output
            expected_value: Expected value

        Returns:
            bool: True if validation passes
        """
        # Use the criterion's validate method
        return criterion.validate(actual_value)

    def validate_exact_match(self, actual: Any, expected: Any) -> bool:
        """
        Validate exact match.

        Args:
            actual: Actual value
            expected: Expected value

        Returns:
            bool: True if values match exactly
        """
        return actual == expected

    def validate_regex(self, actual: str, pattern: str) -> bool:
        """
        Validate using regex pattern.

        Args:
            actual: Actual string value
            pattern: Regex pattern

        Returns:
            bool: True if pattern matches
        """
        try:
            return bool(re.match(pattern, str(actual)))
        except re.error:
            return False

    def validate_similarity(
        self, actual: str, expected: str, threshold: float = 0.8
    ) -> bool:
        """
        Validate semantic similarity.

        Args:
            actual: Actual text
            expected: Expected text
            threshold: Similarity threshold (0-1)

        Returns:
            bool: True if similarity >= threshold
        """
        similarity = self.compute_similarity(str(actual), str(expected))
        return similarity >= threshold

    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute similarity between two strings.

        Uses simple word overlap. In production, use embeddings.

        Args:
            text1: First text
            text2: Second text

        Returns:
            float: Similarity score (0-1)
        """
        # Tokenize
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        # Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        return intersection / union if union > 0 else 0.0

    def validate_custom(
        self, actual: Any, expected: Any, validator_name: str
    ) -> bool:
        """
        Validate using custom validator.

        Args:
            actual: Actual value
            expected: Expected value
            validator_name: Name of registered custom validator

        Returns:
            bool: True if validation passes

        Raises:
            ValueError: If validator not found
        """
        if validator_name not in self.custom_validators:
            raise ValueError(f"Custom validator not found: {validator_name}")

        validator_func = self.custom_validators[validator_name]
        return validator_func(actual, expected)

    def validate_numeric_range(
        self, actual: float, min_value: float, max_value: float
    ) -> bool:
        """
        Validate numeric value is within range.

        Args:
            actual: Actual numeric value
            min_value: Minimum value (inclusive)
            max_value: Maximum value (inclusive)

        Returns:
            bool: True if value is within range
        """
        try:
            value = float(actual)
            return min_value <= value <= max_value
        except (TypeError, ValueError):
            return False

    def validate_list_contains(self, actual: list, expected_items: list) -> bool:
        """
        Validate list contains expected items.

        Args:
            actual: Actual list
            expected_items: Items that should be in the list

        Returns:
            bool: True if all expected items are in actual list
        """
        if not isinstance(actual, list):
            return False

        return all(item in actual for item in expected_items)

    def validate_dict_has_keys(self, actual: dict, expected_keys: list) -> bool:
        """
        Validate dictionary has expected keys.

        Args:
            actual: Actual dictionary
            expected_keys: Keys that should be in the dictionary

        Returns:
            bool: True if all expected keys are present
        """
        if not isinstance(actual, dict):
            return False

        return all(key in actual for key in expected_keys)

    def validate_type(self, actual: Any, expected_type: type) -> bool:
        """
        Validate value is of expected type.

        Args:
            actual: Actual value
            expected_type: Expected type

        Returns:
            bool: True if value is of expected type
        """
        return isinstance(actual, expected_type)

    def categorize_error(self, error: Exception) -> ErrorCategory:
        """
        Categorize an error.

        Args:
            error: Exception that occurred

        Returns:
            ErrorCategory: Category of the error
        """
        error_str = str(error).lower()

        if "timeout" in error_str:
            return ErrorCategory.TIMEOUT
        elif "cost" in error_str:
            return ErrorCategory.COST_EXCEEDED
        elif "format" in error_str or "parse" in error_str:
            return ErrorCategory.FORMAT_ERROR
        elif "missing" in error_str or "not found" in error_str:
            return ErrorCategory.MISSING_OUTPUT
        elif "incorrect" in error_str or "invalid" in error_str:
            return ErrorCategory.INCORRECT_OUTPUT
        else:
            return ErrorCategory.EXCEPTION

    def get_error_message(
        self, category: ErrorCategory, actual: Any, expected: Any
    ) -> str:
        """
        Generate helpful error message.

        Args:
            category: Error category
            actual: Actual value
            expected: Expected value

        Returns:
            str: Helpful error message
        """
        messages = {
            ErrorCategory.TIMEOUT: "Task execution exceeded timeout limit",
            ErrorCategory.COST_EXCEEDED: f"Task cost ${actual:.4f} exceeded limit ${expected:.4f}",
            ErrorCategory.INCORRECT_OUTPUT: f"Output '{actual}' does not match expected '{expected}'",
            ErrorCategory.MISSING_OUTPUT: f"Expected output field '{expected}' is missing",
            ErrorCategory.FORMAT_ERROR: f"Output format is incorrect. Expected: {expected}, Got: {type(actual)}",
            ErrorCategory.EXCEPTION: "An unexpected error occurred during execution",
        }

        return messages.get(category, "Validation failed")


# Predefined custom validators

def validate_json_structure(actual: Any, expected_structure: Dict) -> bool:
    """
    Validate JSON structure matches expected schema.

    Args:
        actual: Actual JSON/dict
        expected_structure: Expected structure (keys and types)

    Returns:
        bool: True if structure matches
    """
    if not isinstance(actual, dict):
        return False

    for key, expected_type in expected_structure.items():
        if key not in actual:
            return False

        if not isinstance(actual[key], expected_type):
            return False

    return True


def validate_financial_metrics(actual: Dict, expected: Dict) -> bool:
    """
    Validate financial metrics with tolerance.

    Args:
        actual: Actual financial metrics
        expected: Expected financial metrics

    Returns:
        bool: True if metrics are within tolerance
    """
    if not isinstance(actual, dict) or not isinstance(expected, dict):
        return False

    tolerance = 0.05  # 5% tolerance for financial metrics

    for key, expected_value in expected.items():
        if key not in actual:
            return False

        try:
            actual_value = float(actual[key])
            expected_value = float(expected_value)

            # Check if within tolerance
            diff = abs(actual_value - expected_value)
            max_diff = abs(expected_value) * tolerance

            if diff > max_diff:
                return False

        except (TypeError, ValueError):
            return False

    return True


def validate_sentiment(actual: str, expected: str) -> bool:
    """
    Validate sentiment classification.

    Args:
        actual: Actual sentiment
        expected: Expected sentiment

    Returns:
        bool: True if sentiments match
    """
    sentiment_map = {
        "positive": ["positive", "good", "happy", "excellent"],
        "negative": ["negative", "bad", "sad", "poor"],
        "neutral": ["neutral", "okay", "moderate"],
    }

    actual_lower = actual.lower()
    expected_lower = expected.lower()

    for sentiment, keywords in sentiment_map.items():
        if expected_lower in keywords and actual_lower in keywords:
            return True

    return actual_lower == expected_lower
