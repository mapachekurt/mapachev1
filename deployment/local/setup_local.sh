#!/bin/bash

################################################################################
# setup_local.sh - Local Environment Setup for Mapache v1
#
# This script sets up a complete local testing environment with:
# - Python dependencies
# - fakeredis for Redis mocking
# - Local SLM (Ollama) with Docker
# - Local config files
# - Test database initialization
# - Prerequisites validation
#
# Usage:
#   ./setup_local.sh [--skip-ollama] [--skip-tests]
#
# Options:
#   --skip-ollama    Skip Ollama Docker setup (if already installed)
#   --skip-tests     Skip running validation tests after setup
#
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOCAL_DIR="${PROJECT_ROOT}/deployment/local"
VENV_DIR="${LOCAL_DIR}/.venv"
CONFIG_DIR="${LOCAL_DIR}/config"
DATA_DIR="${LOCAL_DIR}/data"
LOGS_DIR="${LOCAL_DIR}/logs"

# Parse arguments
SKIP_OLLAMA=false
SKIP_TESTS=false
for arg in "$@"; do
    case $arg in
        --skip-ollama)
            SKIP_OLLAMA=true
            shift
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
    esac
done

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_warning "$1 is not installed"
        return 1
    fi
}

################################################################################
# Pre-flight Checks
################################################################################

preflight_checks() {
    print_header "Pre-flight Checks"

    local all_good=true

    print_step "Checking system prerequisites..."

    # Check Python
    if check_command python3; then
        PYTHON_VERSION=$(python3 --version | awk '{print $2}')
        echo -e "  ${MAGENTA}Version: $PYTHON_VERSION${NC}"
    else
        print_error "Python 3 is required but not installed"
        all_good=false
    fi

    # Check pip
    check_command pip3 || all_good=false

    # Check Docker (optional for Ollama)
    if ! $SKIP_OLLAMA; then
        if check_command docker; then
            echo -e "  ${MAGENTA}Docker version: $(docker --version | awk '{print $3}')${NC}"
        else
            print_warning "Docker not found. Will skip Ollama setup."
            SKIP_OLLAMA=true
        fi
    fi

    # Check git
    check_command git || all_good=false

    if ! $all_good; then
        print_error "Some prerequisites are missing. Please install them first."
        exit 1
    fi

    print_success "All prerequisites satisfied"
}

################################################################################
# Directory Setup
################################################################################

setup_directories() {
    print_header "Setting Up Directory Structure"

    print_step "Creating required directories..."

    mkdir -p "${CONFIG_DIR}"
    mkdir -p "${DATA_DIR}"
    mkdir -p "${LOGS_DIR}"
    mkdir -p "${LOCAL_DIR}/pilot_agents"
    mkdir -p "${LOCAL_DIR}/reports"
    mkdir -p "${LOCAL_DIR}/metrics"

    print_success "Directory structure created"

    echo -e "  ${MAGENTA}Config:  ${CONFIG_DIR}${NC}"
    echo -e "  ${MAGENTA}Data:    ${DATA_DIR}${NC}"
    echo -e "  ${MAGENTA}Logs:    ${LOGS_DIR}${NC}"
}

################################################################################
# Python Environment Setup
################################################################################

setup_python_env() {
    print_header "Setting Up Python Environment"

    print_step "Creating virtual environment..."
    python3 -m venv "${VENV_DIR}"
    print_success "Virtual environment created at ${VENV_DIR}"

    print_step "Activating virtual environment..."
    source "${VENV_DIR}/bin/activate"

    print_step "Upgrading pip..."
    pip install --upgrade pip > /dev/null 2>&1
    print_success "pip upgraded"

    print_step "Installing core dependencies..."
    pip install -q \
        google-cloud-aiplatform \
        google-auth \
        google-cloud-logging \
        google-cloud-trace \
        pydantic \
        pyyaml \
        requests \
        aiohttp \
        asyncio \
        numpy
    print_success "Core dependencies installed"

    print_step "Installing testing dependencies..."
    pip install -q \
        pytest \
        pytest-asyncio \
        pytest-cov \
        pytest-mock
    print_success "Testing dependencies installed"

    print_step "Installing fakeredis for Redis mocking..."
    pip install -q fakeredis[lua]
    print_success "fakeredis installed"

    print_step "Installing local LLM dependencies..."
    pip install -q \
        llama-cpp-python \
        transformers \
        torch
    print_success "Local LLM dependencies installed"

    print_step "Installing observability dependencies..."
    pip install -q \
        opentelemetry-api \
        opentelemetry-sdk \
        opentelemetry-instrumentation \
        structlog
    print_success "Observability dependencies installed"

    print_step "Installing vector store (ChromaDB)..."
    pip install -q chromadb
    print_success "ChromaDB installed"
}

################################################################################
# Ollama Setup
################################################################################

setup_ollama() {
    if $SKIP_OLLAMA; then
        print_warning "Skipping Ollama setup (--skip-ollama flag)"
        return
    fi

    print_header "Setting Up Local SLM (Ollama)"

    print_step "Checking if Ollama container is running..."
    if docker ps | grep -q ollama; then
        print_success "Ollama container already running"
        return
    fi

    print_step "Pulling Ollama Docker image..."
    docker pull ollama/ollama:latest
    print_success "Ollama image pulled"

    print_step "Starting Ollama container..."
    docker run -d \
        --name ollama-local \
        -p 11434:11434 \
        -v "${DATA_DIR}/ollama:/root/.ollama" \
        ollama/ollama:latest
    print_success "Ollama container started"

    print_step "Waiting for Ollama to be ready..."
    sleep 5

    print_step "Pulling Llama 3 model (8B quantized)..."
    docker exec ollama-local ollama pull llama3:8b-instruct-q4_0
    print_success "Llama 3 model pulled"

    print_step "Testing Ollama API..."
    if curl -s http://localhost:11434/api/tags > /dev/null; then
        print_success "Ollama API is responding"
    else
        print_error "Ollama API is not responding"
    fi
}

################################################################################
# Configuration Files
################################################################################

create_config_files() {
    print_header "Creating Configuration Files"

    # Create local.env
    print_step "Creating local.env..."
    cat > "${CONFIG_DIR}/local.env" << 'EOF'
# Mapache v1 - Local Testing Environment Configuration

# Environment
ENVIRONMENT=local
DEBUG=true

# Mock LLM (no real API calls)
USE_MOCK_LLM=true
MOCK_LLM_LATENCY_MS=100

# Local Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:8b-instruct-q4_0

# Redis (using fakeredis)
USE_FAKE_REDIS=true

# Observability
LOG_LEVEL=DEBUG
STRUCTURED_LOGGING=true
ENABLE_TRACING=false  # Disable for local testing
ENABLE_METRICS=true

# Cost tracking
TRACK_COSTS=true
COST_BUDGET_USD=10.00

# Evaluation
RUN_QUALITY_GATES=true
QUALITY_GATE_THRESHOLD=0.85

# Agent Configuration
AGENT_TIMEOUT_SECONDS=30
MAX_RETRIES=3
CIRCUIT_BREAKER_THRESHOLD=5

# Database (SQLite for local)
DB_TYPE=sqlite
DB_PATH=./data/local_test.db

# Feature Flags
ENABLE_CACHING=true
ENABLE_MEMORY=true
ENABLE_COORDINATION=true
EOF
    print_success "local.env created"

    # Create test_config.yaml
    print_step "Creating test_config.yaml..."
    cat > "${CONFIG_DIR}/test_config.yaml" << 'EOF'
# Test Configuration for Local Development

test_suite:
  name: "Mapache v1 Local Test Suite"
  version: "1.0.0"

pilot_agents:
  - name: "freshdesk"
    agent_id: "agent_987"
    category: "support"
    tier: "Specialized Vertical Tools"
  - name: "contentful"
    agent_id: "agent_602"
    category: "content_marketing"
    tier: "Marketing & Sales"

golden_tasks:
  freshdesk:
    - task: "Create a support ticket"
      expected_outcome: "Ticket created successfully"
      max_cost_usd: 0.05
      timeout_ms: 5000
    - task: "List open tickets"
      expected_outcome: "Tickets retrieved"
      max_cost_usd: 0.03
      timeout_ms: 3000
    - task: "Update ticket status"
      expected_outcome: "Status updated"
      max_cost_usd: 0.04
      timeout_ms: 4000

  contentful:
    - task: "Create content entry"
      expected_outcome: "Entry created"
      max_cost_usd: 0.05
      timeout_ms: 5000
    - task: "Retrieve content"
      expected_outcome: "Content retrieved"
      max_cost_usd: 0.03
      timeout_ms: 3000
    - task: "Update content"
      expected_outcome: "Content updated"
      max_cost_usd: 0.04
      timeout_ms: 4000

improvements:
  evaluation:
    enabled: true
    golden_tasks_count: 3
  observability:
    enabled: true
    log_format: "json"
  memory:
    enabled: true
    session_ttl_seconds: 3600
    vector_store: "chromadb"
  coordination:
    enabled: true
    message_broker: "fakeredis"
  cost_optimization:
    enabled: true
    router_strategy: "smart"
    cache_enabled: true
  reliability:
    enabled: true
    retry_enabled: true
    circuit_breaker_enabled: true
  deployment:
    enabled: true
    strategy: "local"

metrics:
  collect_latency: true
  collect_cost: true
  collect_quality: true
  report_interval_seconds: 60
EOF
    print_success "test_config.yaml created"

    # Create mock LLM responses
    print_step "Creating mock LLM responses..."
    cat > "${CONFIG_DIR}/mock_responses.json" << 'EOF'
{
  "default": {
    "response": "This is a mock LLM response for local testing.",
    "latency_ms": 100,
    "cost_usd": 0.001,
    "tokens": 50
  },
  "freshdesk_create_ticket": {
    "response": "Ticket #12345 created successfully with priority: High",
    "latency_ms": 120,
    "cost_usd": 0.002,
    "tokens": 75
  },
  "contentful_create_entry": {
    "response": "Content entry created with ID: entry_abc123",
    "latency_ms": 110,
    "cost_usd": 0.0018,
    "tokens": 65
  }
}
EOF
    print_success "mock_responses.json created"
}

################################################################################
# Database Initialization
################################################################################

initialize_database() {
    print_header "Initializing Test Database"

    print_step "Creating SQLite database..."

    cat > "${DATA_DIR}/init_db.sql" << 'EOF'
-- Test database schema for Mapache v1

CREATE TABLE IF NOT EXISTS agent_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT NOT NULL,
    task TEXT NOT NULL,
    status TEXT NOT NULL,
    latency_ms INTEGER,
    cost_usd REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    agent_id TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS quality_checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT NOT NULL,
    task TEXT NOT NULL,
    passed BOOLEAN NOT NULL,
    score REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_agent_executions_agent_id ON agent_executions(agent_id);
CREATE INDEX IF NOT EXISTS idx_metrics_agent_id ON metrics(agent_id);
CREATE INDEX IF NOT EXISTS idx_quality_checks_agent_id ON quality_checks(agent_id);
EOF

    sqlite3 "${DATA_DIR}/local_test.db" < "${DATA_DIR}/init_db.sql"
    print_success "Database initialized at ${DATA_DIR}/local_test.db"
}

################################################################################
# Prerequisites Validation
################################################################################

validate_setup() {
    print_header "Validating Setup"

    local validation_passed=true

    # Check Python imports
    print_step "Validating Python imports..."
    python3 << 'EOF'
import sys
try:
    import google.cloud.aiplatform
    import pydantic
    import yaml
    import fakeredis
    import chromadb
    import pytest
    print("✓ All Python imports successful")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
EOF
    if [ $? -eq 0 ]; then
        print_success "Python imports validated"
    else
        print_error "Python imports validation failed"
        validation_passed=false
    fi

    # Check config files
    print_step "Validating configuration files..."
    if [ -f "${CONFIG_DIR}/local.env" ] && \
       [ -f "${CONFIG_DIR}/test_config.yaml" ] && \
       [ -f "${CONFIG_DIR}/mock_responses.json" ]; then
        print_success "Configuration files validated"
    else
        print_error "Configuration files missing"
        validation_passed=false
    fi

    # Check database
    print_step "Validating database..."
    if sqlite3 "${DATA_DIR}/local_test.db" "SELECT COUNT(*) FROM agent_executions;" > /dev/null 2>&1; then
        print_success "Database validated"
    else
        print_error "Database validation failed"
        validation_passed=false
    fi

    # Check Ollama (if enabled)
    if ! $SKIP_OLLAMA; then
        print_step "Validating Ollama..."
        if curl -s http://localhost:11434/api/tags > /dev/null; then
            print_success "Ollama validated"
        else
            print_warning "Ollama validation failed (non-critical)"
        fi
    fi

    if $validation_passed; then
        print_success "All validations passed"
    else
        print_error "Some validations failed"
        exit 1
    fi
}

################################################################################
# Run Tests
################################################################################

run_validation_tests() {
    if $SKIP_TESTS; then
        print_warning "Skipping validation tests (--skip-tests flag)"
        return
    fi

    print_header "Running Validation Tests"

    print_step "Creating test script..."
    cat > "${LOCAL_DIR}/test_setup.py" << 'EOF'
"""Test script to validate local setup"""
import sys
sys.path.insert(0, '/home/user/mapachev1')

def test_fakeredis():
    """Test fakeredis is working"""
    import fakeredis
    redis = fakeredis.FakeRedis()
    redis.set('test', 'value')
    assert redis.get('test') == b'value'
    print("✓ fakeredis working")

def test_chromadb():
    """Test ChromaDB is working"""
    import chromadb
    client = chromadb.Client()
    collection = client.create_collection("test")
    assert collection.name == "test"
    print("✓ ChromaDB working")

def test_mock_llm():
    """Test mock LLM configuration"""
    import json
    with open('/home/user/mapachev1/deployment/local/config/mock_responses.json') as f:
        responses = json.load(f)
    assert 'default' in responses
    print("✓ Mock LLM config working")

def test_database():
    """Test database connection"""
    import sqlite3
    conn = sqlite3.connect('/home/user/mapachev1/deployment/local/data/local_test.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM agent_executions")
    count = cursor.fetchone()[0]
    assert count == 0
    conn.close()
    print("✓ Database working")

if __name__ == '__main__':
    try:
        test_fakeredis()
        test_chromadb()
        test_mock_llm()
        test_database()
        print("\n✓ All validation tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Validation test failed: {e}")
        sys.exit(1)
EOF

    python3 "${LOCAL_DIR}/test_setup.py"
    if [ $? -eq 0 ]; then
        print_success "Validation tests passed"
    else
        print_error "Validation tests failed"
        exit 1
    fi
}

################################################################################
# Generate Setup Report
################################################################################

generate_report() {
    print_header "Setup Complete - Summary Report"

    local report_file="${LOCAL_DIR}/reports/setup_report_$(date +%Y%m%d_%H%M%S).txt"

    cat > "${report_file}" << EOF
╔══════════════════════════════════════════════════════════════════════╗
║           MAPACHE V1 - LOCAL SETUP COMPLETE                          ║
╚══════════════════════════════════════════════════════════════════════╝

Setup Date: $(date)
Project Root: ${PROJECT_ROOT}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSTALLED COMPONENTS:
  ✓ Python virtual environment: ${VENV_DIR}
  ✓ Core dependencies: google-cloud-aiplatform, pydantic, yaml
  ✓ Testing dependencies: pytest, pytest-asyncio
  ✓ fakeredis: Redis mocking for local testing
  ✓ ChromaDB: Vector store for memory system
  ✓ Local LLM: llama-cpp-python, transformers
$(if ! $SKIP_OLLAMA; then echo "  ✓ Ollama: Docker container with Llama 3 (8B)"; fi)

DIRECTORY STRUCTURE:
  ${CONFIG_DIR}/     - Configuration files
  ${DATA_DIR}/       - Database and data files
  ${LOGS_DIR}/       - Log files
  ${LOCAL_DIR}/pilot_agents/   - Enhanced pilot agents
  ${LOCAL_DIR}/reports/        - Test and validation reports
  ${LOCAL_DIR}/metrics/        - Metrics and analytics

CONFIGURATION FILES:
  ✓ local.env           - Environment variables
  ✓ test_config.yaml    - Test configuration
  ✓ mock_responses.json - Mock LLM responses

DATABASE:
  ✓ SQLite: ${DATA_DIR}/local_test.db
  ✓ Tables: agent_executions, metrics, quality_checks

VALIDATION STATUS:
  ✓ Python imports working
  ✓ Configuration files present
  ✓ Database initialized
$(if ! $SKIP_OLLAMA; then echo "  ✓ Ollama API responding"; fi)
$(if ! $SKIP_TESTS; then echo "  ✓ Validation tests passed"; fi)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT STEPS:

1. Activate virtual environment:
   source ${VENV_DIR}/bin/activate

2. Load environment variables:
   source ${CONFIG_DIR}/local.env

3. Integrate pilot agents:
   ./deployment/local/integrate_pilot_agents.sh

4. Run tests:
   ./deployment/local/test_pilot_agents.sh

5. Validate improvements:
   ./deployment/local/validate_improvements.sh

6. Collect metrics:
   ./deployment/local/collect_metrics.sh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For more information, see:
  - Documentation: ${PROJECT_ROOT}/README.md
  - Architecture: ${PROJECT_ROOT}/ARCHITECTURE.md
  - Gap Analysis: ${PROJECT_ROOT}/GAP_ANALYSIS.md

╔══════════════════════════════════════════════════════════════════════╗
║                      SETUP SUCCESSFUL! 🚀                            ║
╚══════════════════════════════════════════════════════════════════════╝
EOF

    cat "${report_file}"
    print_success "Setup report saved to: ${report_file}"
}

################################################################################
# Main Execution
################################################################################

main() {
    echo -e "${CYAN}"
    cat << "EOF"
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║              MAPACHE V1 - LOCAL ENVIRONMENT SETUP                    ║
║                                                                      ║
║  Setting up complete local testing environment with:                ║
║    • Python dependencies                                            ║
║    • fakeredis (Redis mocking)                                      ║
║    • Local SLM (Ollama)                                             ║
║    • Configuration files                                            ║
║    • Test database                                                  ║
║    • Validation tests                                               ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"

    preflight_checks
    setup_directories
    setup_python_env
    setup_ollama
    create_config_files
    initialize_database
    validate_setup
    run_validation_tests
    generate_report

    echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  Setup complete! Environment ready for local testing.${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# Run main function
main "$@"
