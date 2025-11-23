"""Pydantic models for type safety across agents."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


# Enums
class RecommendationType(str, Enum):
    """Type of recommendation."""
    BUILD = "build"
    FORK = "fork"
    HYBRID = "hybrid"


class SentimentLevel(str, Enum):
    """Sentiment level categories."""
    VERY_FRUSTRATED = "very_frustrated"
    FRUSTRATED = "frustrated"
    MILD = "mild"
    NEUTRAL = "neutral"


# Validation Agent Models
class ValidationRequest(BaseModel):
    """Request for validation agent."""
    problem_hypothesis: str
    target_subreddits: List[str] = []
    competitors: List[str] = []
    timeframe: str = "week"


class SentimentBreakdown(BaseModel):
    """Breakdown of sentiment analysis."""
    very_frustrated: int = 0
    frustrated: int = 0
    mild: int = 0
    neutral: int = 0


class CompetitorWeakness(BaseModel):
    """Competitor weakness analysis."""
    mention_count: int
    complaints: List[str] = []


class ValidationEvidence(BaseModel):
    """Evidence collected during validation."""
    mention_count: int
    reddit_mentions: int = 0
    twitter_mentions: int = 0
    hackernews_mentions: int = 0
    frustration_score: int = Field(ge=0, le=100)
    urgency_score: int = Field(ge=0, le=100)
    top_quotes: List[str]
    sentiment_breakdown: SentimentBreakdown
    competitor_weaknesses: Dict[str, CompetitorWeakness] = {}


class ValidationResult(BaseModel):
    """Result from validation agent."""
    problem_hypothesis: str
    validation_score: int = Field(ge=0, le=100)
    evidence: ValidationEvidence
    recommendation: str
    timestamp: datetime = Field(default_factory=datetime.now)


# Opportunity Agent Models
class OpportunityRequest(BaseModel):
    """Request for opportunity agent."""
    market_segment: str
    functionality: str
    competitors: List[str] = []
    preferred_language: Optional[str] = None


class MarketSize(BaseModel):
    """Market size calculations."""
    TAM_dollars: int = Field(ge=0)
    SAM_dollars: int = Field(ge=0)
    SOM_dollars: int = Field(ge=0)
    growth_rate_cagr: float = Field(ge=0, le=1)
    market_drivers: List[str] = []
    sources: List[str] = []
    analysis_notes: str = ""


class MarketTrend(BaseModel):
    """Individual market trend."""
    name: str
    description: str
    impact_on_new_entrants: str  # positive/negative/neutral
    adoption_timeline: str  # early/growing/mature
    key_players: List[str] = []


class TrendAnalysis(BaseModel):
    """Market trends analysis."""
    trends: List[MarketTrend] = []
    opportunities: List[str] = []
    threats: List[str] = []


class Competitor(BaseModel):
    """Competitor information."""
    name: str
    overview: str = ""
    key_features: List[str] = []
    pricing_model: str = ""
    target_segment: str = ""
    strengths: List[str] = []
    weaknesses: List[str] = []
    estimated_market_share: str = ""


class CompetitiveLandscape(BaseModel):
    """Competitive landscape analysis."""
    competitors: List[Competitor] = []
    market_positioning: Dict[str, List[str]] = {}
    gaps: List[str] = []
    differentiation_opportunities: List[str] = []
    average_rating: float = 0.0


class OSSProject(BaseModel):
    """Open source project information."""
    name: str
    full_name: str = ""
    url: str
    description: str = ""
    stars: int
    forks: int = 0
    license: str
    language: str = ""
    fork_score: int = Field(ge=0, le=100)
    fork_recommendation: str = ""
    fork_reasons: List[str] = []
    days_since_push: int = 0


class BuildStrategy(BaseModel):
    """Build vs fork strategy recommendation."""
    recommendation: RecommendationType
    rationale: str
    selected_project: Optional[OSSProject] = None
    estimated_time_savings: str
    estimated_cost_savings: str
    risks: List[str] = []
    implementation_strategy: str = ""


class OpportunityResult(BaseModel):
    """Result from opportunity agent."""
    market_segment: str
    functionality: str
    market_size: MarketSize
    trends: TrendAnalysis
    competitive_landscape: CompetitiveLandscape
    oss_recommendations: List[OSSProject] = []
    build_strategy: BuildStrategy
    opportunity_score: int = Field(ge=0, le=100)
    strategic_recommendation: str
    timestamp: datetime = Field(default_factory=datetime.now)


# Orchestrator Agent Models
class OpportunityHypothesis(BaseModel):
    """Single opportunity hypothesis to analyze."""
    problem: str
    market: str
    functionality: str
    subreddits: List[str] = []
    competitors: List[str] = []
    timeframe: str = "week"
    language: Optional[str] = None


class RankedOpportunity(BaseModel):
    """Opportunity with validation and analysis combined."""
    input: OpportunityHypothesis
    validation: ValidationResult
    opportunity: OpportunityResult
    combined_score: float = Field(ge=0, le=100)
    rank: int


class LinearIssue(BaseModel):
    """Linear issue information."""
    id: str
    url: str
    identifier: str
    title: str


class LinearProject(BaseModel):
    """Linear project information."""
    project_id: Optional[str]
    project_url: Optional[str]
    project_name: Optional[str] = None
    issues: List[LinearIssue] = []


class OrchestratorResult(BaseModel):
    """Result from orchestrator agent."""
    ranked_opportunities: List[RankedOpportunity]
    synthesis: str
    linear_project: Optional[LinearProject]
    recommendation: str
    total_analyzed: int
    timestamp: float


# A2A Protocol Models
class A2ASourceAgent(BaseModel):
    """Source agent information in A2A request."""
    id: str
    endpoint: str


class A2ARequest(BaseModel):
    """A2A protocol request."""
    protocol_version: str = "1.0"
    source_agent: A2ASourceAgent
    capability: str
    payload: Dict[str, Any]
    request_id: str


class A2AResponse(BaseModel):
    """A2A protocol response."""
    protocol_version: str = "1.0"
    request_id: str
    agent_id: str
    capability: str
    status: str  # success or error
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
