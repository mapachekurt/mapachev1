#!/bin/bash
#
# Start Local A2A Demo
#
# This script starts the registry service and several example agents
# for local testing and demonstration.
#

set -e

echo "========================================="
echo "Starting A2A Local Demo"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
REGISTRY_PORT=8080
AGENT_START_PORT=8001

# Cleanup function
cleanup() {
    echo ""
    echo "${YELLOW}Stopping all services...${NC}"
    pkill -f "python.*infrastructure/registry/main.py" || true
    pkill -f "python.*agents.*agent.py" || true
    echo "${GREEN}Cleanup complete${NC}"
}

# Register cleanup on exit
trap cleanup EXIT INT TERM

# Start registry service
echo "${GREEN}Starting Registry Service on port ${REGISTRY_PORT}...${NC}"
cd "$(dirname "$0")/.."
export PYTHONPATH="${PWD}:${PYTHONPATH}"
export REGISTRY_PORT=${REGISTRY_PORT}
python -m infrastructure.registry.main &
REGISTRY_PID=$!
echo "Registry PID: ${REGISTRY_PID}"

# Wait for registry to be ready
echo "Waiting for registry to start..."
for i in {1..30}; do
    if curl -s http://localhost:${REGISTRY_PORT}/health > /dev/null 2>&1; then
        echo "${GREEN}Registry is ready!${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "Registry failed to start"
        exit 1
    fi
    sleep 1
done

echo ""
echo "${GREEN}Registry Service running at: http://localhost:${REGISTRY_PORT}${NC}"
echo ""

# Populate registry with agent cards
echo "${GREEN}Populating registry with agent cards...${NC}"
python scripts/populate_registry.py

echo ""
echo "========================================="
echo "Services Started Successfully!"
echo "========================================="
echo ""
echo "Registry Service:  http://localhost:${REGISTRY_PORT}"
echo "Agent Cards:       http://localhost:${REGISTRY_PORT}/agents"
echo "Health Check:      http://localhost:${REGISTRY_PORT}/health"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Keep script running
wait
