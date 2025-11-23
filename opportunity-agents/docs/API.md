# API Documentation

Complete API reference for all three opportunity discovery agents.

## Table of Contents

- [Validation Agent API](#validation-agent-api)
- [Opportunity Agent API](#opportunity-agent-api)
- [Orchestrator Agent API](#orchestrator-agent-api)
- [Shared Models](#shared-models)

---

## Validation Agent API

### POST /a2a/validate

Validate a problem hypothesis by collecting social media evidence.

**Endpoint:** `{VALIDATION_AGENT_ENDPOINT}/a2a/validate`

**Headers:**
```
Content-Type: application/json
A2A-Protocol-Version: 1.0
```

**Request Body:**
```json
{
  "problem": "construction equipment tracking",
  "subreddits": ["construction", "contractors"],
  "competitors": ["ToolTracker", "EquipmentManager"],
  "timeframe": "month"
}
```

**Parameters:**
- `problem` (string, required): Problem hypothesis to validate
- `subreddits` (array, optional): List of subreddit names to search
- `competitors` (array, optional): List of competitor names
- `timeframe` (string, optional): week|month|year (default: "week")

**Response:**
```json
{
  "problem_hypothesis": "construction equipment tracking",
  "validation_score": 87,
  "evidence": {
    "mention_count": 123,
    "reddit_mentions": 89,
    "twitter_mentions": 24,
    "hackernews_mentions": 10,
    "frustration_score": 89,
    "urgency_score": 82,
    "top_quotes": [
      "We waste 2 hours daily looking for equipment",
      "Current solutions are too expensive for small contractors",
      "Nothing works offline on job sites"
    ],
    "sentiment_breakdown": {
      "very_frustrated": 45,
      "frustrated": 30,
      "mild": 10,
      "neutral": 5
    },
    "competitor_weaknesses": {
      "ToolTracker": {
        "mention_count": 15,
        "complaints": [
          "Too expensive for small contractors",
          "Mobile app crashes frequently",
          "Poor offline support"
        ]
      }
    }
  },
  "recommendation": "🟢 STRONG VALIDATION: Build immediately.",
  "timestamp": "2025-01-23T10:30:00Z"
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid request
- `500` - Server error

---

## Opportunity Agent API

### POST /a2a/analyze

Analyze market opportunity and recommend build strategy.

**Endpoint:** `{OPPORTUNITY_AGENT_ENDPOINT}/a2a/analyze`

**Headers:**
```
Content-Type: application/json
A2A-Protocol-Version: 1.0
```

**Request Body:**
```json
{
  "market": "construction management software",
  "functionality": "equipment tracking with offline mobile support",
  "competitors": ["ToolTracker", "EquipmentManager"],
  "language": "Python"
}
```

**Parameters:**
- `market` (string, required): Market segment description
- `functionality` (string, required): What you want to build
- `competitors` (array, optional): List of competitor names
- `language` (string, optional): Preferred programming language

**Response:**
```json
{
  "market_segment": "construction management software",
  "functionality": "equipment tracking with offline mobile support",
  "opportunity_score": 82,
  "market_size": {
    "TAM_dollars": 4700000000,
    "SAM_dollars": 1200000000,
    "SOM_dollars": 85000000,
    "growth_rate_cagr": 0.18,
    "market_drivers": [
      "Digital transformation in construction",
      "Labor shortage driving automation",
      "Rising equipment costs"
    ],
    "sources": [
      "Market Research Report 2025",
      "Construction Tech Review"
    ]
  },
  "competitive_landscape": {
    "competitors": [
      {
        "name": "ToolTracker",
        "pricing_model": "Per-user/month",
        "strengths": ["Market leader", "Brand recognition"],
        "weaknesses": ["Expensive", "Poor mobile experience"]
      }
    ],
    "gaps": [
      "Affordable solution for small contractors",
      "True offline-first mobile experience"
    ],
    "differentiation_opportunities": [
      "Freemium pricing for small teams",
      "Offline-first architecture",
      "Simple, focused feature set"
    ]
  },
  "oss_recommendations": [
    {
      "name": "inventory-tracker",
      "url": "https://github.com/example/inventory-tracker",
      "stars": 1500,
      "license": "MIT",
      "fork_score": 85,
      "fork_recommendation": "🟢 Excellent fork candidate",
      "fork_reasons": [
        "Recently active (10 days since push)",
        "Permissive license (MIT)",
        "Active community (45 contributors)"
      ]
    }
  ],
  "build_strategy": {
    "recommendation": "fork",
    "rationale": "Strong OSS option available with 85/100 fork score...",
    "selected_project": { /* OSS project details */ },
    "estimated_time_savings": "3-4 months",
    "estimated_cost_savings": "$50,000-$75,000",
    "risks": [
      "Need to customize for construction industry",
      "May need to add offline sync"
    ],
    "implementation_strategy": "Fork inventory-tracker, add construction-specific features..."
  },
  "strategic_recommendation": "🟢 STRONG OPPORTUNITY: FORK strategy recommended.",
  "timestamp": "2025-01-23T10:30:00Z"
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid request
- `500` - Server error

---

## Orchestrator Agent API

### POST /a2a/discover

Coordinate validation and opportunity analysis for multiple hypotheses.

**Endpoint:** `{ORCHESTRATOR_AGENT_ENDPOINT}/a2a/discover`

**Headers:**
```
Content-Type: application/json
A2A-Protocol-Version: 1.0
```

**Request Body:**
```json
{
  "opportunities": [
    {
      "problem": "construction equipment tracking",
      "market": "construction management software",
      "functionality": "equipment tracking with offline mobile",
      "subreddits": ["construction", "contractors"],
      "competitors": ["ToolTracker"],
      "timeframe": "month",
      "language": "Python"
    },
    {
      "problem": "restaurant inventory waste",
      "market": "restaurant management software",
      "functionality": "automated inventory tracking",
      "subreddits": ["restaurateur"],
      "competitors": ["MarketMan"]
    }
  ]
}
```

**Parameters:**
- `opportunities` (array, required): List of opportunity hypotheses to analyze

**Response:**
```json
{
  "ranked_opportunities": [
    {
      "rank": 1,
      "input": { /* original request */ },
      "validation": { /* validation agent result */ },
      "opportunity": { /* opportunity agent result */ },
      "combined_score": 84.5
    }
  ],
  "synthesis": "Executive summary of findings...",
  "linear_project": {
    "project_id": "proj_abc123",
    "project_url": "https://linear.app/team/project/abc123",
    "project_name": "Build: construction equipment tracking",
    "issues": [
      {
        "id": "ISS-1",
        "url": "https://linear.app/team/issue/ISS-1",
        "identifier": "ISS-1",
        "title": "📋 Research & Requirements Definition"
      }
    ]
  },
  "recommendation": "🟢 STRONG RECOMMENDATION: BUILD IMMEDIATELY...",
  "total_analyzed": 2,
  "timestamp": 1706012400.123
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid request
- `500` - Server error

---

## Shared Models

### ValidationEvidence

```typescript
{
  mention_count: number;
  reddit_mentions: number;
  twitter_mentions: number;
  hackernews_mentions: number;
  frustration_score: number;  // 0-100
  urgency_score: number;      // 0-100
  top_quotes: string[];
  sentiment_breakdown: {
    very_frustrated: number;
    frustrated: number;
    mild: number;
    neutral: number;
  };
  competitor_weaknesses: {
    [competitor: string]: {
      mention_count: number;
      complaints: string[];
    }
  };
}
```

### MarketSize

```typescript
{
  TAM_dollars: number;
  SAM_dollars: number;
  SOM_dollars: number;
  growth_rate_cagr: number;  // decimal (0.15 = 15%)
  market_drivers: string[];
  sources: string[];
  analysis_notes: string;
}
```

### BuildStrategy

```typescript
{
  recommendation: "build" | "fork" | "hybrid";
  rationale: string;
  selected_project?: OSSProject;
  estimated_time_savings: string;
  estimated_cost_savings: string;
  risks: string[];
  implementation_strategy: string;
}
```

---

## Rate Limits

- Validation Agent: 100 requests/hour per API key
- Opportunity Agent: 100 requests/hour per API key
- Orchestrator Agent: 50 requests/hour per API key

## Error Handling

All agents return errors in this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

Common error codes:
- `INVALID_REQUEST` - Malformed request
- `MISSING_PARAMETERS` - Required parameters missing
- `RATE_LIMIT_EXCEEDED` - Too many requests
- `AGENT_UNAVAILABLE` - Target agent not responding
- `INTERNAL_ERROR` - Server error

## Authentication

Currently using A2A protocol headers for agent identification. Future versions will support:
- API key authentication
- OAuth 2.0
- JWT tokens

---

For more details, see:
- [A2A Specification](A2A_SPEC.md)
- [Usage Guide](USAGE.md)
