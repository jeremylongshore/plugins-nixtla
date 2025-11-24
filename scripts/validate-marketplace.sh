#!/bin/bash
# validate-marketplace.sh
# Validates Claude Code marketplace structure and plugin configurations

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MARKETPLACE_FILE="$REPO_ROOT/.claude-plugin/marketplace.json"
ERRORS=0
WARNINGS=0

echo "========================================"
echo "Claude Code Marketplace Validator"
echo "========================================"
echo ""

# Color codes
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Check if marketplace.json exists
echo "[1/5] Checking marketplace.json existence..."
if [ ! -f "$MARKETPLACE_FILE" ]; then
    echo -e "${RED}ERROR: marketplace.json not found at $MARKETPLACE_FILE${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✓ marketplace.json found${NC}"
fi

# Validate JSON syntax
echo "[2/5] Validating marketplace.json syntax..."
if command -v jq &> /dev/null; then
    if jq empty "$MARKETPLACE_FILE" 2>/dev/null; then
        echo -e "${GREEN}✓ Valid JSON syntax${NC}"
    else
        echo -e "${RED}ERROR: Invalid JSON syntax in marketplace.json${NC}"
        ((ERRORS++))
    fi
else
    echo -e "${YELLOW}WARNING: jq not installed, skipping JSON validation${NC}"
    ((WARNINGS++))
fi

# Check required marketplace fields
echo "[3/5] Checking required marketplace fields..."
REQUIRED_FIELDS=("name" "owner" "plugins")
for field in "${REQUIRED_FIELDS[@]}"; do
    if jq -e ".$field" "$MARKETPLACE_FILE" &>/dev/null; then
        echo -e "${GREEN}✓ Required field '$field' present${NC}"
    else
        echo -e "${RED}ERROR: Required field '$field' missing${NC}"
        ((ERRORS++))
    fi
done

# Validate plugin entries
echo "[4/5] Validating plugin entries..."
PLUGIN_COUNT=$(jq '.plugins | length' "$MARKETPLACE_FILE")
echo "Found $PLUGIN_COUNT plugin(s)"

for i in $(seq 0 $((PLUGIN_COUNT - 1))); do
    PLUGIN_NAME=$(jq -r ".plugins[$i].name" "$MARKETPLACE_FILE")
    echo ""
    echo "  Validating plugin: $PLUGIN_NAME"

    # Check plugin.json if strict mode is enabled
    STRICT=$(jq -r ".plugins[$i].strict // true" "$MARKETPLACE_FILE")
    PLUGIN_SOURCE=$(jq -r ".plugins[$i].source" "$MARKETPLACE_FILE")
    PLUGIN_ROOT=$(jq -r ".metadata.pluginRoot // \"./plugins\"" "$MARKETPLACE_FILE")
    PLUGIN_PATH="$REPO_ROOT/$PLUGIN_ROOT/$PLUGIN_SOURCE/.claude-plugin/plugin.json"

    if [ "$STRICT" = "true" ]; then
        if [ -f "$PLUGIN_PATH" ]; then
            echo -e "  ${GREEN}✓ plugin.json found at $PLUGIN_PATH${NC}"

            # Validate plugin.json syntax
            if jq empty "$PLUGIN_PATH" 2>/dev/null; then
                echo -e "  ${GREEN}✓ Valid plugin.json syntax${NC}"
            else
                echo -e "  ${RED}ERROR: Invalid JSON in plugin.json${NC}"
                ((ERRORS++))
            fi
        else
            echo -e "  ${YELLOW}WARNING: plugin.json not found (strict=true)${NC}"
            echo -e "  ${YELLOW}  Expected: $PLUGIN_PATH${NC}"
            ((WARNINGS++))
        fi
    else
        echo -e "  ${YELLOW}⚠ Strict mode disabled (plugin.json optional)${NC}"
    fi

    # Check plugin directory exists
    PLUGIN_DIR="$REPO_ROOT/$PLUGIN_ROOT/$PLUGIN_SOURCE"
    if [ -d "$PLUGIN_DIR" ]; then
        echo -e "  ${GREEN}✓ Plugin directory exists: $PLUGIN_DIR${NC}"
    else
        echo -e "  ${RED}ERROR: Plugin directory not found: $PLUGIN_DIR${NC}"
        ((ERRORS++))
    fi
done

# Summary
echo ""
echo "[5/5] Validation Summary"
echo "========================================"

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ Marketplace validation PASSED${NC}"
    echo -e "${GREEN}  0 errors${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}  $WARNINGS warning(s)${NC}"
    fi
    exit 0
else
    echo -e "${RED}✗ Marketplace validation FAILED${NC}"
    echo -e "${RED}  $ERRORS error(s)${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}  $WARNINGS warning(s)${NC}"
    fi
    exit 1
fi
