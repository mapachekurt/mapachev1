"""Local Small Language Model for routine task execution.

This module provides the LocalSLM class which handles routine tasks locally
without requiring API calls to cloud-based LLMs, reducing costs.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List, Tuple
import re
import hashlib
from datetime import datetime


@dataclass
class TaskPattern:
    """Pattern for identifying routine tasks."""

    pattern: str
    task_type: str
    confidence_threshold: float = 0.8
    template_response: Optional[str] = None


@dataclass
class LocalResponse:
    """Response from local SLM execution."""

    content: str
    confidence: float
    task_type: str
    execution_time_ms: float
    used_local_model: bool


class LocalSLM:
    """Local Small Language Model for handling routine tasks.

    This class identifies and executes routine tasks locally using
    pattern matching and template-based responses, avoiding costly
    API calls for simple, repetitive tasks.
    """

    def __init__(self) -> None:
        """Initialize the local SLM with task patterns and templates."""
        self._task_patterns: List[TaskPattern] = [
            # Greeting patterns
            TaskPattern(
                pattern=r"\b(hello|hi|hey|greetings)\b",
                task_type="greeting",
                confidence_threshold=0.9,
                template_response="Hello! I'm here to help. What can I do for you?"
            ),
            # Status check patterns
            TaskPattern(
                pattern=r"\b(status|health|alive|ping|check)\b",
                task_type="status_check",
                confidence_threshold=0.85,
                template_response="System is operational. All agents are ready."
            ),
            # Simple calculation patterns
            TaskPattern(
                pattern=r"\b(calculate|compute|add|subtract|multiply|divide)\b.*\d+",
                task_type="calculation",
                confidence_threshold=0.8
            ),
            # Data formatting patterns
            TaskPattern(
                pattern=r"\b(format|convert|transform)\b.*(json|csv|yaml|xml)",
                task_type="formatting",
                confidence_threshold=0.75
            ),
            # Simple extraction patterns
            TaskPattern(
                pattern=r"\b(extract|get|find)\b.*(email|url|phone|date)",
                task_type="extraction",
                confidence_threshold=0.8
            ),
            # List/enumerate patterns
            TaskPattern(
                pattern=r"\b(list|show|display|enumerate)\b",
                task_type="listing",
                confidence_threshold=0.7
            ),
            # Translation patterns (simple)
            TaskPattern(
                pattern=r"\btranslate\b.*(to|into)\s+(spanish|french|german)",
                task_type="translation",
                confidence_threshold=0.75
            ),
            # Summary patterns (short text)
            TaskPattern(
                pattern=r"\b(summarize|tldr|brief)\b",
                task_type="summary",
                confidence_threshold=0.7
            ),
        ]

        # Response templates for common tasks
        self._templates: Dict[str, str] = {
            "greeting": "Hello! I'm here to help. What can I do for you?",
            "status_check": "System is operational. All agents are ready.",
            "fallback": "I can help with that. Let me process your request."
        }

        # Track execution statistics
        self._stats: Dict[str, int] = {
            "total_requests": 0,
            "handled_locally": 0,
            "delegated_to_llm": 0
        }

    def is_routine_task(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, float, str]:
        """Determine if a task is routine and can be handled locally.

        Args:
            prompt: The user's request text
            context: Optional context information

        Returns:
            Tuple of (is_routine, confidence, task_type)
        """
        context = context or {}
        prompt_lower = prompt.lower().strip()

        # Check if prompt is too long (likely complex)
        if len(prompt.split()) > 50:
            return False, 0.0, "unknown"

        # Check if requires complex reasoning
        complex_indicators = [
            "analyze", "evaluate", "design", "architect", "optimize",
            "explain why", "how does", "what if", "compare and contrast"
        ]
        if any(indicator in prompt_lower for indicator in complex_indicators):
            return False, 0.0, "complex"

        # Match against task patterns
        best_match: Optional[TaskPattern] = None
        best_confidence = 0.0

        for pattern in self._task_patterns:
            if re.search(pattern.pattern, prompt_lower, re.IGNORECASE):
                # Calculate confidence based on pattern match strength
                confidence = self._calculate_confidence(prompt, pattern)

                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = pattern

        if best_match and best_confidence >= best_match.confidence_threshold:
            return True, best_confidence, best_match.task_type

        return False, best_confidence, "unknown"

    def execute(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None
    ) -> LocalResponse:
        """Execute a routine task locally.

        Args:
            prompt: The user's request text
            context: Optional context information

        Returns:
            LocalResponse with the execution result
        """
        start_time = datetime.now()
        context = context or {}

        self._stats["total_requests"] += 1

        # Check if task is routine
        is_routine, confidence, task_type = self.is_routine_task(prompt, context)

        if not is_routine:
            self._stats["delegated_to_llm"] = self._stats.get("delegated_to_llm", 0) + 1
            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return LocalResponse(
                content="Task requires full LLM processing",
                confidence=0.0,
                task_type="complex",
                execution_time_ms=execution_time,
                used_local_model=False
            )

        self._stats["handled_locally"] += 1

        # Execute based on task type
        response_content = self._execute_task(prompt, task_type, context)

        execution_time = (datetime.now() - start_time).total_seconds() * 1000

        return LocalResponse(
            content=response_content,
            confidence=confidence,
            task_type=task_type,
            execution_time_ms=execution_time,
            used_local_model=True
        )

    def _execute_task(
        self,
        prompt: str,
        task_type: str,
        context: Dict[str, Any]
    ) -> str:
        """Execute a specific task type.

        Args:
            prompt: The user's request text
            task_type: Type of task to execute
            context: Context information

        Returns:
            Response content
        """
        if task_type == "greeting":
            return self._handle_greeting(prompt, context)
        elif task_type == "status_check":
            return self._handle_status_check(prompt, context)
        elif task_type == "calculation":
            return self._handle_calculation(prompt, context)
        elif task_type == "extraction":
            return self._handle_extraction(prompt, context)
        elif task_type == "listing":
            return self._handle_listing(prompt, context)
        elif task_type == "formatting":
            return self._handle_formatting(prompt, context)
        else:
            return self._templates.get(task_type, self._templates["fallback"])

    def _handle_greeting(self, prompt: str, context: Dict[str, Any]) -> str:
        """Handle greeting tasks."""
        user_name = context.get("user_name", "")
        if user_name:
            return f"Hello {user_name}! I'm here to help. What can I do for you?"
        return self._templates["greeting"]

    def _handle_status_check(self, prompt: str, context: Dict[str, Any]) -> str:
        """Handle status check tasks."""
        agent_count = context.get("agent_count", 0)
        if agent_count:
            return f"System is operational. {agent_count} agents are ready and available."
        return self._templates["status_check"]

    def _handle_calculation(self, prompt: str, context: Dict[str, Any]) -> str:
        """Handle simple calculation tasks."""
        # Extract numbers from prompt
        numbers = re.findall(r'\d+\.?\d*', prompt)

        if len(numbers) < 2:
            return "I can help with calculations. Please provide the numbers to calculate."

        try:
            num1, num2 = float(numbers[0]), float(numbers[1])

            prompt_lower = prompt.lower()
            if "add" in prompt_lower or "+" in prompt or "plus" in prompt_lower:
                result = num1 + num2
                return f"The sum is: {result}"
            elif "subtract" in prompt_lower or "-" in prompt or "minus" in prompt_lower:
                result = num1 - num2
                return f"The difference is: {result}"
            elif "multiply" in prompt_lower or "*" in prompt or "times" in prompt_lower:
                result = num1 * num2
                return f"The product is: {result}"
            elif "divide" in prompt_lower or "/" in prompt:
                if num2 == 0:
                    return "Cannot divide by zero."
                result = num1 / num2
                return f"The quotient is: {result}"
            else:
                return f"Found numbers {num1} and {num2}. Please specify the operation."

        except (ValueError, IndexError):
            return "I can help with calculations. Please provide valid numbers."

    def _handle_extraction(self, prompt: str, context: Dict[str, Any]) -> str:
        """Handle simple extraction tasks."""
        text = context.get("text", prompt)

        if "email" in prompt.lower():
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
            if emails:
                return f"Found emails: {', '.join(emails)}"
            return "No email addresses found."

        if "url" in prompt.lower() or "link" in prompt.lower():
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            if urls:
                return f"Found URLs: {', '.join(urls)}"
            return "No URLs found."

        if "phone" in prompt.lower():
            phones = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
            if phones:
                return f"Found phone numbers: {', '.join(phones)}"
            return "No phone numbers found."

        return "I can extract emails, URLs, or phone numbers. Please specify what to extract."

    def _handle_listing(self, prompt: str, context: Dict[str, Any]) -> str:
        """Handle listing tasks."""
        items = context.get("items", [])
        if items:
            formatted = "\n".join(f"- {item}" for item in items)
            return f"Here are the items:\n{formatted}"
        return "I can help list items. Please provide the items to list."

    def _handle_formatting(self, prompt: str, context: Dict[str, Any]) -> str:
        """Handle simple formatting tasks."""
        return "I can help with data formatting. For complex formatting, please use the full LLM."

    def _calculate_confidence(self, prompt: str, pattern: TaskPattern) -> float:
        """Calculate confidence score for a pattern match.

        Args:
            prompt: The user's request text
            pattern: The task pattern to match against

        Returns:
            Confidence score between 0.0 and 1.0
        """
        confidence = 0.5  # Base confidence

        # Check pattern match strength
        if re.search(pattern.pattern, prompt, re.IGNORECASE):
            confidence += 0.3

        # Shorter prompts are more likely to be routine
        word_count = len(prompt.split())
        if word_count <= 10:
            confidence += 0.2
        elif word_count <= 20:
            confidence += 0.1

        # Penalize complex language
        complex_words = ["however", "therefore", "consequently", "nevertheless"]
        if any(word in prompt.lower() for word in complex_words):
            confidence -= 0.2

        return min(1.0, max(0.0, confidence))

    def get_stats(self) -> Dict[str, Any]:
        """Get execution statistics.

        Returns:
            Dictionary with execution statistics
        """
        total = self._stats["total_requests"]
        local_rate = (self._stats["handled_locally"] / total * 100) if total > 0 else 0

        return {
            "total_requests": total,
            "handled_locally": self._stats["handled_locally"],
            "delegated_to_llm": self._stats["delegated_to_llm"],
            "local_handling_rate": round(local_rate, 2)
        }

    def add_task_pattern(self, pattern: TaskPattern) -> None:
        """Add a new task pattern for routine task detection.

        Args:
            pattern: Task pattern to add
        """
        self._task_patterns.append(pattern)

    def add_template(self, task_type: str, template: str) -> None:
        """Add a response template for a task type.

        Args:
            task_type: Type of task
            template: Response template
        """
        self._templates[task_type] = template
