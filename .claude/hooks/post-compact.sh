#!/bin/bash
# Post-Compact Hook for Nixtla Skills Repository
# Automatically reminds Claude Code to read validator and standards after compaction
#
# This hook runs after every conversation compaction in Claude Code.
# It ensures Claude always has access to the latest validation rules and skill standards.

echo "📚 POST-COMPACT: Loading Nixtla Skills Standards..."
echo ""
echo "CRITICAL DOCUMENTS TO READ:"
echo "  1. scripts/validate_skills.py - Production validator (14 critical fixes)"
echo "  2. 000-docs/skills-schema/SKILLS-STANDARD-COMPLETE.md - v2.3.0 ENGINEERING-COMPLETE"
echo ""
echo "KEY VALIDATION RULES:"
echo "  - Description: ≤1024 chars (NOT 200!), third-person, plain text"
echo "  - Body: ≤5000 words"
echo "  - Total budget: <15,000 chars across ALL skills"
echo "  - Paths: Use {baseDir}, no hardcoded /home/ or /Users/"
echo "  - when_to_use: DEPRECATED (warn if used)"
echo "  - Version: Recommended (semantic versioning)"
echo ""
echo "SOURCES (by authority):"
echo "  1. Anthropic Platform Docs (official)"
echo "  2. Lee Han Chung Oct 2025 (newest implementation guide)"
echo "  3. Official Anthropic Blog"
echo "  4. Engineering Blog"
echo ""
echo "Run validator: python scripts/validate_skills.py"
echo ""
