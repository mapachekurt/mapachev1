# Usage Guide

Comprehensive guide for using the Opportunity Discovery Agent System.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Running Agents Locally](#running-agents-locally)
3. [Using Individual Agents](#using-individual-agents)
4. [Orchestrating Multiple Agents](#orchestrating-multiple-agents)
5. [Deploying to Production](#deploying-to-production)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### 1. Set Up Environment

```bash
# Clone repository
git clone <repository-url>
cd opportunity-agents

# Copy environment template
cp .env.example .env
```

### 2. Configure API Keys

Edit `.env` and add your API keys:

```bash
# Required
GOOGLE_API_KEY=your-google-api-key
REDDIT_CLIENT_ID=your-reddit-id
REDDIT_CLIENT_SECRET=your-reddit-secret

# Optional but recommended
TWITTER_BEARER_TOKEN=your-twitter-token
GITHUB_TOKEN=your-github-token
LINEAR_API_KEY=your-linear-key
```

### 3. Install Dependencies

```bash
# Install for all agents
pip install -r validation-agent/requirements.txt
pip install -r opportunity-agent/requirements.txt
pip install -r orchestrator-agent/requirements.txt
```

### 4. Verify Installation

```bash
# Run tests
pytest validation-agent/tests/
pytest opportunity-agent/tests/
pytest orchestrator-agent/tests/
```

---

## Running Agents Locally

### Validation Agent

Validate if people are suffering from a specific problem:

```bash
cd validation-agent
python main.py "construction equipment tracking"
```

**Output:**
```
🔍 Validating opportunity: construction equipment tracking
📊 Searching 3 subreddits over the past month

1️⃣ Collecting Reddit mentions...
   ✓ Found 89 Reddit mentions

2️⃣ Searching Twitter...
   ✓ Found 24 Twitter mentions

3️⃣ Searching HackerNews...
   ✓ Found 15 stories, 12 comments

4️⃣ Analyzing sentiment...
   ✓ Frustration score: 85/100
   ✓ Urgency score: 78/100

5️⃣ Analyzing 2 competitors...
   ✓ ToolTracker: 18 mentions

6️⃣ Calculating validation score...
   ✓ Final validation score: 87/100

✅ 🟢 STRONG VALIDATION: High demand with clear pain points. Build immediately.
```

### Opportunity Agent

Analyze market opportunity and build strategy:

```bash
cd opportunity-agent
python main.py "construction management software" "equipment tracking with offline mobile"
```

**Output:**
```
🔍 Analyzing opportunity: construction management software
💡 Functionality: equipment tracking with offline mobile

1️⃣ Calculating market size (TAM/SAM/SOM)...
   ✓ TAM: $4,700,000,000
   ✓ SAM: $1,200,000,000
   ✓ SOM: $85,000,000
   ✓ Growth: 18.0% CAGR

2️⃣ Analyzing market trends...
   ✓ Identified 5 key trends

3️⃣ Analyzing 2 competitors...
   ✓ Analyzed 2 competitors
   ✓ Found 5 differentiation opportunities

4️⃣ Searching for relevant OSS projects...
   ✓ Found 8 relevant OSS projects
   ✓ Top project: inventory-tracker (85/100 fork score)

5️⃣ Generating build vs fork recommendation...
   ✓ Recommendation: FORK
   ✓ Time savings: 3-4 months

6️⃣ Calculating opportunity score...
   ✓ Opportunity score: 82/100

✅ 🟢 STRONG OPPORTUNITY: FORK strategy recommended. Large market with exploitable gaps.
```

### Orchestrator Agent

Coordinate both agents for complete analysis:

```bash
cd orchestrator-agent
python main.py
```

Uses example opportunities from `main.py`. To analyze custom opportunities:

```bash
python main.py "your problem" "your market" "your functionality" "subreddit1,subreddit2" "competitor1,competitor2"
```

---

## Using Individual Agents

### Validation Agent Examples

#### Minimum Usage

```python
from validation_agent.main import ValidationAgent

agent = ValidationAgent()

result = agent.validate_opportunity(
    problem_hypothesis="restaurant inventory waste",
    target_subreddits=["restaurateur"]
)

print(f"Validation Score: {result['validation_score']}/100")
```

#### With Competitors

```python
result = agent.validate_opportunity(
    problem_hypothesis="equipment tracking",
    target_subreddits=["construction", "contractors"],
    competitors=["ToolTracker", "EquipmentManager"],
    timeframe="month"
)

# Access competitor weaknesses
for competitor, data in result['evidence']['competitor_weaknesses'].items():
    print(f"{competitor}:")
    for complaint in data['complaints']:
        print(f"  - {complaint}")
```

#### Analyze Specific Quotes

```python
result = agent.validate_opportunity(
    problem_hypothesis="inventory management",
    target_subreddits=["restaurateur"],
    timeframe="year"
)

# Get top pain point quotes
for i, quote in enumerate(result['evidence']['top_quotes'][:5], 1):
    print(f"{i}. \"{quote}\"")
```

### Opportunity Agent Examples

#### Basic Market Analysis

```python
from opportunity_agent.main import OpportunityAgent

agent = OpportunityAgent()

result = agent.analyze_opportunity(
    market_segment="construction management software",
    functionality="equipment tracking"
)

print(f"Market Size (TAM): ${result['market_size']['TAM_dollars']:,}")
print(f"Opportunity Score: {result['opportunity_score']}/100")
```

#### With OSS Recommendations

```python
result = agent.analyze_opportunity(
    market_segment="restaurant management",
    functionality="inventory tracking",
    preferred_language="Python"
)

# Get top OSS project
if result['oss_recommendations']:
    top_project = result['oss_recommendations'][0]
    print(f"Top OSS: {top_project['name']}")
    print(f"Fork Score: {top_project['fork_score']}/100")
    print(f"License: {top_project['license']}")
```

#### Competitor Analysis

```python
result = agent.analyze_opportunity(
    market_segment="construction software",
    functionality="equipment tracking",
    competitors=["ToolTracker", "EquipmentManager", "AssetTrack"]
)

# Access competitive insights
for gap in result['competitive_landscape']['gaps']:
    print(f"Market Gap: {gap}")

for opp in result['competitive_landscape']['differentiation_opportunities']:
    print(f"Opportunity: {opp}")
```

---

## Orchestrating Multiple Agents

### Basic Orchestration

```python
import asyncio
from orchestrator_agent.main import OrchestratorAgent

async def analyze():
    agent = OrchestratorAgent()

    result = await agent.discover_opportunities([
        {
            "problem": "equipment tracking",
            "market": "construction software",
            "functionality": "offline mobile tracking",
            "subreddits": ["construction"],
            "competitors": ["ToolTracker"]
        }
    ])

    # Access results
    top = result['ranked_opportunities'][0]
    print(f"Combined Score: {top['combined_score']}/100")
    print(f"Validation: {top['validation']['validation_score']}/100")
    print(f"Opportunity: {top['opportunity']['opportunity_score']}/100")

    # Linear project (if created)
    if result['linear_project']:
        print(f"Linear Project: {result['linear_project']['project_url']}")

asyncio.run(analyze())
```

### Comparing Multiple Opportunities

```python
async def compare_opportunities():
    agent = OrchestratorAgent()

    result = await agent.discover_opportunities([
        {
            "problem": "equipment tracking",
            "market": "construction software",
            "functionality": "offline tracking",
            "subreddits": ["construction"]
        },
        {
            "problem": "inventory waste",
            "market": "restaurant software",
            "functionality": "predictive ordering",
            "subreddits": ["restaurateur"]
        },
        {
            "problem": "scheduling chaos",
            "market": "salon software",
            "functionality": "automated booking",
            "subreddits": ["salon", "beauty"]
        }
    ])

    # Print ranked list
    for opp in result['ranked_opportunities']:
        print(f"#{opp['rank']}: {opp['input']['problem']}")
        print(f"  Score: {opp['combined_score']}/100")
        print(f"  Recommendation: {opp['validation']['recommendation']}")
        print()

    # Executive synthesis
    print("EXECUTIVE SUMMARY:")
    print(result['synthesis'])

asyncio.run(compare_opportunities())
```

### Single Opportunity Analysis

```python
async def quick_analysis():
    agent = OrchestratorAgent()

    result = await agent.analyze_single_opportunity(
        problem="equipment tracking",
        market="construction software",
        functionality="offline mobile tracking",
        subreddits=["construction", "contractors"],
        competitors=["ToolTracker"],
        language="Python"
    )

    print(result['synthesis'])
    if result['linear_project']:
        print(f"\nLinear: {result['linear_project']['project_url']}")

asyncio.run(quick_analysis())
```

---

## Deploying to Production

### 1. Configure GCP

```bash
# Set environment variables
export GCP_PROJECT_ID=your-project-id
export GCP_REGION=us-central1

# Authenticate
gcloud auth login
gcloud config set project $GCP_PROJECT_ID
```

### 2. Deploy Agents

```bash
# Make deployment script executable
chmod +x deployment/deploy.sh

# Deploy all agents
./deployment/deploy.sh
```

### 3. Verify Deployment

```bash
# Check agent endpoints
cat deployment/endpoints.env

# Test orchestrator
curl -X POST ${ORCHESTRATOR_AGENT_ENDPOINT}/a2a/discover \
  -H "Content-Type: application/json" \
  -H "A2A-Protocol-Version: 1.0" \
  -d '{"opportunities": [...]}'
```

### 4. Set Up Monitoring

```bash
# Enable logging
gcloud logging read "resource.type=cloud_run_revision" --limit 50

# Set up alerts
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="Agent Errors" \
  --condition-threshold-value=10 \
  --condition-threshold-duration=60s
```

---

## Best Practices

### 1. Validation Agent

**DO:**
- Use specific, focused problem hypotheses
- Include relevant subreddits (3-5 is optimal)
- Specify competitors if known
- Use longer timeframes (month/year) for better data

**DON'T:**
- Use vague problem statements
- Include too many subreddits (>10)
- Run too frequently (respect API rate limits)

### 2. Opportunity Agent

**DO:**
- Provide detailed market descriptions
- Include realistic competitors
- Specify preferred language for OSS search
- Review OSS projects manually before forking

**DON'T:**
- Rely solely on automated market sizing
- Ignore competitive analysis
- Fork OSS without reviewing license

### 3. Orchestrator Agent

**DO:**
- Analyze 2-5 opportunities at a time
- Review synthesis before acting
- Check combined score thresholds (>50 recommended)
- Validate Linear project creation

**DON'T:**
- Analyze >10 opportunities at once (slow)
- Skip manual validation of top opportunity
- Automatically commit to low-score opportunities

### 4. General

**DO:**
- Store API keys in environment variables
- Enable debug logging for troubleshooting
- Run tests before deployment
- Monitor API usage and costs

**DON'T:**
- Commit API keys to repository
- Run in production without testing
- Ignore rate limits

---

## Troubleshooting

### Common Issues

#### 1. "Reddit API Error: 401 Unauthorized"

**Cause:** Invalid Reddit credentials

**Solution:**
```bash
# Verify credentials
echo $REDDIT_CLIENT_ID
echo $REDDIT_CLIENT_SECRET

# Re-create Reddit app at https://www.reddit.com/prefs/apps
# Update .env with new credentials
```

#### 2. "No OSS projects found"

**Cause:** GitHub API rate limit or invalid search

**Solution:**
```bash
# Check GitHub token
echo $GITHUB_TOKEN

# Verify rate limit
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit

# Try broader search terms
```

#### 3. "Linear project creation failed"

**Cause:** Invalid Linear API key or team ID

**Solution:**
```bash
# Test Linear API
curl https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ viewer { id name } }"}'

# Get team ID from Linear settings
```

#### 4. "Agent timeout"

**Cause:** Network issues or slow API responses

**Solution:**
```python
# Increase timeout
result = await router.call_validation_agent(
    request,
    timeout=120  # 2 minutes
)
```

#### 5. "Low validation scores"

**Cause:** Problem not well-defined or lack of online discussion

**Solution:**
- Refine problem hypothesis
- Try different subreddits
- Extend timeframe to "year"
- Validate problem manually first

### Debug Mode

Enable detailed logging:

```bash
export DEBUG=true
export LOG_LEVEL=DEBUG

python orchestrator-agent/main.py
```

### Testing Locally Without APIs

```python
# Use mock data for testing
from unittest.mock import Mock

# Mock validation agent
validation_agent.reddit.search_pain_points = Mock(return_value={
    "mentions": 50,
    "posts": [...]
})
```

---

## Support

- **Documentation:** Check [API.md](API.md) and [A2A_SPEC.md](A2A_SPEC.md)
- **Issues:** Open GitHub issue with logs and error messages
- **Email:** your-email@example.com

---

For API reference, see [API.md](API.md)
