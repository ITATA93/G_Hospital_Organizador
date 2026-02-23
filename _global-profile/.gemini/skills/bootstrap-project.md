# Skill: Bootstrap Project Configuration

## Description
Analyzes the current project and generates optimal configuration for VS Code (extensions, settings) and Antigravity Agents. This skill transforms a raw codebase into a fully configured development environment.

## Usage
```bash
gemini "Bootstrap this project"
gemini "Configura este proyecto"
gemini /bootstrap
```

## Procedure

1.  **Analyze Project Type**
    *   Check for `package.json` (Node.js/Frontend).
    *   Check for `requirements.txt`, `pyproject.toml` (Python).
    *   Check for `go.mod` (Go).
    *   Check for `Cargo.toml` (Rust).
    *   Check for `docker-compose.yml` (Docker).

2.  **Determine Profile**
    *   **Frontend**: If React, Vue, Angular found.
    *   **Backend**: If Django, FastAPI, Express found.
    *   **Data Science**: If pandas, numpy, jupyter found.

3.  **Generate `.vscode/extensions.json`**
    *   Recommend extensions based on analysis (e.g., 'ms-python.python', 'dbaeumer.vscode-eslint').

4.  **Generate `.vscode/settings.json`**
    *   Configure formatters (Black, Prettier).
    *   Set file exclusions.

5.  **Generate `.gemini/settings.json`**
    *   Create or update project-specific agent settings.
    *   Enable/Disable execution capabilities based on profile.

## Example Output (`.vscode/extensions.json`)
```json
{
  "recommendations": [
    "ms-python.python",
    "charliermarsh.ruff",
    "tamasfe.even-better-toml"
  ]
}
```

## Example Action
> "I detected this is a **Python/FastAPI** project. I will now:
> 1. Create `.vscode/extensions.json` recommending Python + Ruff.
> 2. Configure `.gemini/settings.json` with the 'Backend-Secure' profile.
> 3. Add a 'Run Server' task to `.vscode/tasks.json`."
