# Opportunity Discovery Agent System

A three-agent system for discovering, validating, and analyzing business opportunities using Google ADK and A2A (Agent-to-Agent) standards.

## 🎯 Overview

This system consists of three interoperable AI agents:

1. **Validation Agent** - Social listening and pain point evidence collection
2. **Opportunity Agent** - Strategic market analysis and OSS leverage recommendations
3. **Orchestrator Agent** - A2A coordination and synthesis

Each agent can run independently or coordinate via A2A protocol for comprehensive opportunity analysis.

## ✨ Features

### Validation Agent
- Multi-platform scraping (Reddit, Twitter/X, HackerNews, G2)
- Sentiment analysis with frustration scoring (0-100)
- Competitor weakness detection
- Evidence aggregation and validation scoring

### Opportunity Agent
- TAM/SAM/SOM calculation using Google Search grounding
- Competitive landscape mapping
- OSS codebase analysis via GitHub API
- Build vs. Fork recommendations with time/cost estimates

### Orchestrator Agent
- Parallel agent coordination via A2A protocol
- Multi-opportunity ranking and synthesis
- Linear project creation with acceptance criteria
- Executive summary generation

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Google Cloud account with Vertex AI access
- API keys for: Google AI, Reddit, Twitter, GitHub, Linear

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd opportunity-agents
```

2. Install dependencies for each agent:
```bash
# Validation Agent
cd validation-agent
pip install -r requirements.txt

# Opportunity Agent
cd ../opportunity-agent
pip install -r requirements.txt

# Orchestrator Agent
cd ../orchestrator-agent
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Running Locally

#### Test Individual Agents

```bash
# Validation Agent
cd validation-agent
python main.py "construction equipment tracking"

# Opportunity Agent
cd opportunity-agent
python main.py "construction management software" "equipment tracking with offline mobile"

# Orchestrator Agent (coordinates both)
cd orchestrator-agent
python main.py
```

#### Run Full Orchestration

```bash
cd orchestrator-agent
python main.py "test problem" "test market" "test functionality"
```

## 📋 Example Use Case

```python
from orchestrator-agent.main import OrchestratorAgent
import asyncio

async def discover_opportunities():
    agent = OrchestratorAgent()

    result = await agent.discover_opportunities([
        {
            "problem": "construction equipment tracking",
            "market": "construction management software",
            "functionality": "equipment tracking with offline mobile",
            "subreddits": ["construction", "contractors"],
            "competitors": ["ToolTracker", "EquipmentManager"]
        }
    ])

    print(f"Top Opportunity Score: {result['ranked_opportunities'][0]['combined_score']}/100")
    print(f"Linear Project: {result['linear_project']['project_url']}")

asyncio.run(discover_opportunities())
```

## 🏗️ Architecture

```
opportunity-agents/
├── validation-agent/        # Social listening & validation
│   ├── agent.yaml
│   ├── main.py
│   ├── tools/
│   │   ├── reddit_scraper.py
│   │   ├── twitter_api.py
│   │   ├── hackernews_api.py
│   │   ├── g2_reviews.py
│   │   └── sentiment_analyzer.py
│   └── tests/
│
├── opportunity-agent/       # Market analysis & strategy
│   ├── agent.yaml
│   ├── main.py
│   ├── tools/
│   │   ├── market_analyzer.py
│   │   ├── competitor_intel.py
│   │   ├── oss_finder.py
│   │   └── build_fork_advisor.py
│   └── tests/
│
├── orchestrator-agent/      # Agent coordination
│   ├── agent.yaml
│   ├── main.py
│   ├── tools/
│   │   ├── agent_router.py
│   │   ├── result_synthesizer.py
│   │   └── linear_creator.py
│   └── tests/
│
├── shared/                  # Shared utilities
│   ├── a2a_client.py       # A2A protocol implementation
│   ├── models.py           # Pydantic models
│   └── utils.py
│
└── deployment/              # Deployment configs
    ├── deploy.sh
    └── cloudbuild.yaml
```

## 📖 Documentation

- [API Documentation](docs/API.md) - REST API endpoints and parameters
- [A2A Specification](docs/A2A_SPEC.md) - Agent-to-Agent protocol details
- [Usage Guide](docs/USAGE.md) - Detailed usage instructions

## 🚢 Deployment

### Deploy to GCP Vertex AI

```bash
# Set environment variables
export GCP_PROJECT_ID=your-project-id
export GCP_REGION=us-central1

# Run deployment script
chmod +x deployment/deploy.sh
./deployment/deploy.sh
```

### CI/CD with Cloud Build

The system includes automatic testing and deployment via Google Cloud Build:

```bash
# Trigger build on commit
git push origin main
```

## 🧪 Testing

Run tests for each agent:

```bash
# All agents
pytest validation-agent/tests/ -v
pytest opportunity-agent/tests/ -v
pytest orchestrator-agent/tests/ -v
```

## 💰 Cost Estimates

Monthly costs at scale (100 customers):

- Vertex AI Agent Engine: ~$2,500
- Gemini API calls: ~$1,200
- External APIs (Twitter, etc.): ~$100
- Cloud Run: ~$200
- Storage & Monitoring: ~$200

**Total: ~$4,500/month**

**Break-even: 92 customers @ $49/month**

## 🔒 Security

- All API keys stored in environment variables
- No credentials committed to repository
- HTTPS-only communication between agents
- A2A protocol includes source verification

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

[Your License Here]

## 🆘 Support

- Documentation: `docs/`
- Issues: GitHub Issues
- Email: your-email@example.com

## 🎓 Credits

Built using:
- [Google ADK](https://cloud.google.com/agent-engine/docs)
- [A2A Protocol](https://a2aprotocol.org)
- [Gemini 2.0](https://ai.google.dev)
- [PRAW](https://praw.readthedocs.io) - Reddit API
- [Linear API](https://developers.linear.app)

## 🗺️ Roadmap

- [ ] Add more social platforms (ProductHunt, IndieHackers)
- [ ] Implement caching for API calls
- [ ] Add webhook support for async notifications
- [ ] Build web dashboard for results visualization
- [ ] Support for multi-language analysis
- [ ] Integration with additional project management tools

---

**Made with ❤️ using Google ADK and A2A standards**
