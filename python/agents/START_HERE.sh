#!/bin/bash
# Run verification of agent army reference material files.

set -e
ls -la _reference_materials/
cat _reference_materials/AGENT_INVENTORY_COMPLETE.yaml | head -20
