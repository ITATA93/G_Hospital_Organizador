# Implementation Plan - Bootstrap Skill

Enable "Intelligent Bootstrap" for projects, automating the configuration of environment tools (VS Code) and Agent Profiles.

## User Review Required
> [!NOTE]
> This skill will be added to the Global Profile. It requires the `install-global.ps1` script to be run (or the new Symlink feature) to take effect in local projects.

## Proposed Changes

### Global Profile (`_global-profile/.gemini/skills/`)
#### [NEW] [bootstrap-project.md](file:///c:/_Repositorio/AG_Plantilla/_global-profile/.gemini/skills/bootstrap-project.md)
Create a new skill that:
1.  **Analyzes** the current project (files, dependencies).
2.  **Asks** the user for the desired automation level (Basic/Full).
3.  **Generates**:
    *   `.vscode/extensions.json` (Recommended extensions)
    *   `.vscode/settings.json` (Editor settings)
    *   `.gemini/settings.json` (Agent Profile)

### Template (`_template/`)
#### [MODIFY] [init-project.ps1](file:///c:/_Repositorio/AG_Plantilla/_template/init-project.ps1)
Update the `Next Steps` message to include running the bootstrap skill.

#### [MODIFY] [TODO.md](file:///c:/_Repositorio/AG_Plantilla/_template/workspace/docs/TODO.md)
Add a checklist item:
- `[ ] Run 'gemini /bootstrap' to configure VS Code and Agents`

## Verification Plan

### Manual Verification
1.  **Create Test Project**: Run `.\init-project.ps1 "TestBootstrap"`.
2.  **Run Skill**: Inside `TestBootstrap`, run `gemini "Bootstrapea este proyecto"`.
3.  **Verify Output**:
    *   Check if `.vscode/extensions.json` was created.
    *   Check if `.gemini/settings.json` was updated/created.
