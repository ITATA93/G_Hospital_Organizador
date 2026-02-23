# Skill: Deep Research

## Purpose
Execute comprehensive research on topics using Gemini Deep Research API.

## Capabilities
- Multi-source research
- Cited sources
- Structured reports
- Saved to docs/research/

## Requirements
- `GEMINI_API_KEY` (for Gemini Deep Research)
- OR `OPENAI_API_KEY` (for Codex Research)

## Usage
### Gemini (Standard)
```bash
gemini /research "your research question"
```

### Codex (Cost-Effective)
```bash
codex /research "your research question"
```

## Script
Located at: `.gemini/scripts/deep-research.sh` (Auto-detects provider based on invocation)

## Process
### Gemini Provider
1. Submit query to Deep Research API (Google).
2. Wait for completion (2-5 minutes).

### Codex Provider (Simulated)
1. Uses `search_web` tool to gather contexts.
2. Uses `codex` model (GPT-4o/o1-mini) to synthesize.
3. Generates report locally.
3. Parse and format results
4. Save to docs/research/research-TIMESTAMP.md
5. Present executive summary

## Output Format
```markdown
# Deep Research: {query}

_Date: YYYY-MM-DD HH:MM_

---

## Executive Summary
[Key findings in 3-5 bullet points]

## Detailed Findings
[Full research content]

## Sources
[Cited sources with links]

## Recommendations
[How to apply findings to current project]
```

## Rate Limits
- Free tier: 5 researches/day
- Paid tier: Check your plan
