# Deep Research: Antigravity Base Knowledge 2026

*Executed by: Codex Protocol (Simulated)*
*Date: 2026-02-02 23:25*

---

## Executive Summary
This document consolidates the foundational knowledge required to operate and extend the Antigravity Ecosystem.
*   **Agent Architecture**: Moving from "Orchestration" (Centralized Gemini) to "Choreography" (Autonomous Claude/Codex agents).
*   **MCP Protocol**: The "USB-C" of AI. Best practice is to run servers with **Least Privilege** and stateless designs.
*   **VS Code Profiles**: The key to context switching. Profiles isolate extensions and settings, preventing "Extension Hell".

---

## 1. Agentic Design Patterns
Antigravity uses a hybrid model of **Orchestration** and **Choreography**.

### A. Orchestration (The "Manager")
*   **Role**: Gemini (The Architect).
*   **Function**: Explicit command-and-control.
*   **Pattern**: User -> Gemini -> Tool -> Gemini.
*   **Pros**: Easie to debug, state is centralized.
*   **Cons**: Single point of failure (if Gemini gets confused, the chain stops).

### B. Choreography (The "Swarm")
*   **Role**: Claude & Sub-agents.
*   **Function**: Event-driven reaction.
*   **Pattern**: Gemini writes plan -> Claude reads file -> Claude executes test -> Claude fixes bug.
*   **Pros**: Highly scalable, resilient.
*   **Antigravity Implementation**: We use file-based signaling (`TODO.md`, `task.md`) to coordinate agents without a central server.

---

## 2. Model Context Protocol (MCP) Best Practices
MCP is how we connect agents to tools (Git, DB, FileSystem).

### Key Principles
1.  **Statelessness**: Tools should not "remember" the previous call.
    *   *Bad*: `git.commit()` (Assuming files were staged).
    *   *Good*: `git_commit(files=["a.py"], message="fix")`.
2.  **Least Privilege**:
    *   Do not give the agent "Root" access.
    *   Example: The `filesystem` server limits access to `C:\_Repositorio\AG_Proyectos`.
3.  **Client-Host Isolation**:
    *   The MCP client (Gemini) runs in a separate process from the Server (Node/Python). If the tool crashes, the brain survives.

---

## 3. VS Code Advanced Profiles
We solve the "Too Many Extensions" problem with Profiles.

### The Problem
A "Full Stack Developer" installs Python, Node, Java, Docker, Kubernetes, and C++ extensions. VS Code uses 4GB RAM and takes 20s to start.

### The Solution: Role-Based Profiles
1.  **Antigravity-Core**:
    *   Extensions: `cline` (or equivalent), `gitlens`.
    *   Settings: Minimal UI, High performance.
2.  **Python-Backend**:
    *   Extensions: `ms-python`, `ruff`.
    *   Settings: `formatOnSave: true`.
3.  **Frontend-Creative**:
    *   Extensions: `es7-react-snippets`, `tailwind-intellisense`, `prettier`.

### Automation
*   **Settings Sync**: Profiles sync across devices.
*   **Project Association**: Add `"window.profile": "Python-Backend"` to `.vscode/settings.json` (Workspace) to force a profile switch when opening the folder.

---

## 4. Recommendations for Antigravity
1.  **Adopt Hybrid Orchestration**: Keep Gemini as the "Boss" in `task.md` but let Claude be the "Worker" in the terminal.
2.  **Strict MCP Isolation**: Audit `settings.json` to ensure no overlapping tool permissions.
3.  **Profile Enforcers**: Update `bootstrap-project` skill to *auto-generate* a VS Code `.code-profile` file for the user to import.
