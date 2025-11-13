#!/bin/bash
# Run verification of agent army reference material files.
# IMPORTANT: This script must be run from the python/agents/ directory.

set -e
ls -la _reference_materials/
head -20 _reference_materials/AGENT_INVENTORY_COMPLETE.yaml
