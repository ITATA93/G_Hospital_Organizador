# Vendor Capabilities & Skill Matrix

This document provides a *deep technical analysis* of the AI Vendors supported by Antigravity, detailing their internal architecture, executable capabilities, and configuration nuances.

---

## 1. Vendor Comparison Matrix (Deep Dive)

| Feature | **Gemini (Google)** | **Claude (Anthropic)** | **Codex (OpenAI/Legacy)** |
| :--- | :--- | :--- | :--- |
| **Model Family** | Gemini 1.5 Pro/Flash | Claude 3.5 Sonnet/Opus | GPT-4o / o1-mini |
| **Primary Role** | **Architect & Strategist** | **Autonomous Agent** | **Tactical Executor** |
| **Context Window** | **1M - 2M Tokens** | ~200k Tokens | ~128k Tokens |
| **Reasoning** | **Thinking Mode** (Hidden Chain) | Explicit Chain-of-Thought | Standard / Reinforced |
| **Tooling API** | Native Function Calling | Native MCP Support | **Simulated / Injectable** |
| **Cost Profile** | High Efficiency (Flash) | Premium (Sonnet) | **Free/Included (via Copilot)** |
| **Config File** | `.gemini/settings.json` | `.claude/config.json` | `.codex/settings.json` |

---

## 2. Detailed Capabilities

### 🟢 Gemini: The Architect
Gemini is the "brain" that initializes projects. Its massive context window allows it to read *every file in your repo* simultaneously.
*   **Killer Feature**: `codebase_investigator`. It doesn't grep; it *reads*.
*   **Best For**:
    *   Whole-repo Refactoring.
    *   Writing "The Bible" (`CORE_CONCEPTS.md`).
    *   Deep Logic Analysis (finding race conditions across 50 files).

### 🟣 Claude: The Engineer
Claude is the "agent" that lives in the terminal. It excels at *doing*.
*   **Killer Feature**: `bash` & `mcp-hub`. Claude handles git, docker, and databases like a human senior engineer.
*   **Best For**:
    *   "Deploy this to Vercel."
    *   "Debug this failing test suite."
    *   "Review this Pull Request."

### 🔵 Codex: The Researcher & Mechanic
Codex (often GPT-4o via OpenAI) is the highly accessible, low-latency engine.
*   **New role in Antigravity**: **Cost-Effective Deep Research**.
*   **Killer Feature**: `search_web` integration. It synthesizes web results faster and cheaper than the others.
*   **Best For**:
    *   **Deep Research**: "Find the best library for X".
    *   **Quick Scripts**: "Write a regex for email."
    *   **Unit Tests**: "Generate coverage for this file."

---

## 3. Skill Configuration Guide

Skills are "Muscle Memory" for agents. Here is how to configure them per vendor.

### A. Anatomy of a Skill
A skill file (e.g., `deep-research.md`) must contain:
1.  **Frontmatter**: Description.
2.  **Usage**: How to invoke it.
3.  **Procedure**: The step-by-step logic.

### B. Configuring for Gemini
Gemini allows **Thinking Mode** skills.
*   **Location**: `.gemini/skills/`
*   **Format**: Narrative Markdown.
*   **Tip**: Use blockquotes `> like this` to simulate the agent's internal monologue instructions.

### C. Configuring for Claude
Claude uses **Tool Definitions** (MCP).
*   **Location**: `.claude/skills/`
*   **Format**: strict JSON or Markdown with `input_schema`.
*   **Tip**: Claude loves clearly defined inputs.
    ```json
    { "type": "string", "description": "The search query" }
    ```

### D. Configuring for Codex
Codex relies on **System Prompt Injection**.
*   **Location**: `.codex/skills/`
*   **Format**: Plain text instructions.
*   **Tip**: Keep it short. Codex context is smaller.
    *   *Bad*: "Analyze the history of philosophy..."
    *   *Good*: "Search web for X. Summarize top 5 links."

---

## 4. Deep Research Configuration (Codex Special)
To enable the **Codex Deep Research** workflow requested by users:

1.  **Ensure API Key**: Set `OPENAI_API_KEY` in `.env`.
2.  **Verify Tool**: Ensure `search_web` tool is enabled in `.codex/settings.json` (or global config).
3.  **Run**:
    ```bash
    codex /research "Query"
    ```
    *This triggers the `deep-research.md` skill, forcing the 'Codex Provider' path.*
