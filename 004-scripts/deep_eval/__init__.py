"""
Intent Solutions Deep Evaluation Engine

Multi-layer quality assessment for Claude Code plugin skills.
Extends the Universal Validator with LLM-powered analysis,
statistical confidence intervals, and competitive ranking.

Layers:
  1. Static dimension scoring (deterministic, fast)
  2. LLM quality assessment via Groq (Llama 3.3 70B)
  3. Competitive ranking (Elo system)

Author: Jeremy Longshore <jeremy@intentsolutions.io>
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Jeremy Longshore <jeremy@intentsolutions.io>"
