"""Shared utilities and models for opportunity agents."""

from .a2a_client import A2AClient, A2AServer, A2AError
from .models import (
    ValidationRequest,
    ValidationResult,
    ValidationEvidence,
    OpportunityRequest,
    OpportunityResult,
    MarketSize,
    BuildStrategy,
    OrchestratorResult,
    RankedOpportunity,
    LinearProject,
)
from .utils import (
    load_env_file,
    format_currency,
    format_percentage,
    sanitize_filename,
    save_json,
    load_json,
    ColoredOutput,
)

__all__ = [
    # A2A Protocol
    "A2AClient",
    "A2AServer",
    "A2AError",

    # Models
    "ValidationRequest",
    "ValidationResult",
    "ValidationEvidence",
    "OpportunityRequest",
    "OpportunityResult",
    "MarketSize",
    "BuildStrategy",
    "OrchestratorResult",
    "RankedOpportunity",
    "LinearProject",

    # Utilities
    "load_env_file",
    "format_currency",
    "format_percentage",
    "sanitize_filename",
    "save_json",
    "load_json",
    "ColoredOutput",
]
