#!/bin/bash
# Local testing script for intelligence system components
#
# Usage: ./test-local.sh [COMPONENT]
# Components: hackernews, reddit, producthunt, blogs, arxiv, github, analyzer, chief

set -e

COMPONENT=${1:-hackernews}

echo "Testing $COMPONENT locally..."

cd mapachev1

# Set up environment
export GCP_PROJECT_ID="${GCP_PROJECT_ID:-mapache-intelligence-prod}"
export GCP_REGION="${GCP_REGION:-europe-west1}"

case $COMPONENT in
  hackernews)
    echo "Running HackerNews scraper..."
    python -m app.intelligence.scrapers.hackernews
    ;;
  reddit)
    echo "Running Reddit scraper..."
    python -m app.intelligence.scrapers.reddit
    ;;
  producthunt)
    echo "Running ProductHunt scraper..."
    python -m app.intelligence.scrapers.producthunt
    ;;
  blogs)
    echo "Running Blog scraper..."
    python -m app.intelligence.scrapers.blogs
    ;;
  arxiv)
    echo "Running ArXiv scraper..."
    python -m app.intelligence.scrapers.arxiv
    ;;
  github)
    echo "Running GitHub scraper..."
    python -m app.intelligence.scrapers.github
    ;;
  analyzer)
    echo "Testing Gemini analyzer..."
    python -c "
from app.intelligence.processors.gemini_analyzer import analyzer
test_content = {
    'source': 'hackernews',
    'content_type': 'discussion',
    'title': 'Test Article',
    'url': 'https://example.com',
    'content': 'Test content about AI and machine learning',
    'metadata': {},
    'scraped_at': '2025-01-01T00:00:00',
}
result = analyzer.analyze_content(test_content)
print(f'Analysis result: {result}')
"
    ;;
  chief)
    echo "Testing Chief Agent..."
    python -c "
from app.intelligence.chief_agent.agent import chief_agent
result = chief_agent.run_daily_briefing()
print(f'Chief Agent result: {result}')
"
    ;;
  *)
    echo "Unknown component: $COMPONENT"
    echo "Available: hackernews, reddit, producthunt, blogs, arxiv, github, analyzer, chief"
    exit 1
    ;;
esac

echo ""
echo "✅ Test completed!"
