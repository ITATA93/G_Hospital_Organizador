<#
.SYNOPSIS
    Installs Antigravity global profile to user's home directory.

.DESCRIPTION
    This script copies the Antigravity global profile configuration
    to ~/.gemini so it's available for all projects.

.PARAMETER Force
    Overwrite existing configuration if it exists.

.PARAMETER Backup
    Create backup of existing configuration before overwriting.

.EXAMPLE
    .\install-global.ps1
    .\install-global.ps1 -Force
    .\install-global.ps1 -Force -Backup
#>

param(
    [switch]$Force = $false,
    [switch]$Backup = $false
)

$ErrorActionPreference = "Stop"

# Colors
function Write-Success { param($msg) Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Warning { param($msg) Write-Host "[!!] $msg" -ForegroundColor Yellow }
function Write-Info { param($msg) Write-Host "[..] $msg" -ForegroundColor Cyan }
function Write-Error { param($msg) Write-Host "[XX] $msg" -ForegroundColor Red }

Write-Host ""
Write-Host "=============================================" -ForegroundColor Magenta
Write-Host "  ANTIGRAVITY GLOBAL PROFILE INSTALLER" -ForegroundColor Magenta
Write-Host "=============================================" -ForegroundColor Magenta
Write-Host ""

# Paths
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceGemini = Join-Path $scriptDir ".gemini"
$sourceClaude = Join-Path $scriptDir ".claude"
$sourceCodex = Join-Path $scriptDir ".codex"

$homeDir = $env:USERPROFILE
$targetGemini = Join-Path $homeDir ".gemini"
$targetClaude = Join-Path $homeDir ".claude"
$targetCodex = Join-Path $homeDir ".codex"

Write-Info "Source: $scriptDir"
Write-Info "Target: $homeDir"

# Check source exists
if (-not (Test-Path $sourceGemini)) {
    Write-Error "Source .gemini directory not found: $sourceGemini"
    exit 1
}

# ============================================
# PHASE 1: Handle existing configuration
# ============================================
Write-Host ""
Write-Host "--- Phase 1: Checking existing configuration ---" -ForegroundColor Yellow

$geminiExists = Test-Path $targetGemini
$claudeExists = Test-Path $targetClaude
$codexExists = Test-Path $targetCodex

if ($geminiExists -or $claudeExists -or $codexExists) {
    if (-not $Force) {
        Write-Warning "Existing configuration found:"
        if ($geminiExists) { Write-Warning "  - $targetGemini" }
        if ($claudeExists) { Write-Warning "  - $targetClaude" }
        if ($codexExists) { Write-Warning "  - $targetCodex" }
        Write-Error "Use -Force to overwrite or -Force -Backup to backup first"
        exit 1
    }

    if ($Backup) {
        $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

        if ($geminiExists) {
            $backupGemini = "$targetGemini.backup-$timestamp"
            Move-Item $targetGemini $backupGemini
            Write-Success "Backed up: $backupGemini"
        }

        if ($claudeExists) {
            $backupClaude = "$targetClaude.backup-$timestamp"
            Move-Item $targetClaude $backupClaude
            Write-Success "Backed up: $backupClaude"
        }

        if ($codexExists) {
            $backupCodex = "$targetCodex.backup-$timestamp"
            Move-Item $targetCodex $backupCodex
            Write-Success "Backed up: $backupCodex"
        }
    } else {
        if ($geminiExists) {
            Remove-Item -Recurse -Force $targetGemini
            Write-Warning "Removed existing: $targetGemini"
        }
        if ($claudeExists) {
            Remove-Item -Recurse -Force $targetClaude
            Write-Warning "Removed existing: $targetClaude"
        }
        if ($codexExists) {
            Remove-Item -Recurse -Force $targetCodex
            Write-Warning "Removed existing: $targetCodex"
        }
    }
}

# ============================================
# PHASE 2: Copy configuration
# ============================================
Write-Host ""
Write-Host "--- Phase 2: Installing configuration ---" -ForegroundColor Yellow

# Copy .gemini
Copy-Item -Recurse $sourceGemini $targetGemini
Write-Success "Installed: ~/.gemini/"

# Copy .claude if exists
if (Test-Path $sourceClaude) {
    Copy-Item -Recurse $sourceClaude $targetClaude
    Write-Success "Installed: ~/.claude/"
}

# Copy .codex if exists
if (Test-Path $sourceCodex) {
    Copy-Item -Recurse $sourceCodex $targetCodex
    Write-Success "Installed: ~/.codex/"
}

# Copy GEMINI.md to home if it doesn't exist
$sourceGeminiMd = Join-Path $scriptDir "GEMINI.md"
$targetGeminiMd = Join-Path $homeDir "GEMINI.md"
if ((Test-Path $sourceGeminiMd) -and -not (Test-Path $targetGeminiMd)) {
    Copy-Item $sourceGeminiMd $targetGeminiMd
    Write-Success "Installed: ~/GEMINI.md"
}

# ============================================
# PHASE 3: Verify installation
# ============================================
Write-Host ""
Write-Host "--- Phase 3: Verifying installation ---" -ForegroundColor Yellow

$checks = @(
    @{ Path = "$targetGemini\settings.json"; Name = "settings.json" }
    @{ Path = "$targetGemini\agents"; Name = "agents/" }
    @{ Path = "$targetGemini\commands"; Name = "commands/" }
    @{ Path = "$targetGemini\rules"; Name = "rules/" }
)

$allOk = $true
foreach ($check in $checks) {
    if (Test-Path $check.Path) {
        Write-Success "Found: $($check.Name)"
    } else {
        Write-Warning "Missing: $($check.Name)"
        $allOk = $false
    }
}

# ============================================
# SUMMARY
# ============================================
Write-Host ""
if ($allOk) {
    Write-Host "=============================================" -ForegroundColor Green
    Write-Host "  INSTALLATION COMPLETE!" -ForegroundColor Green
    Write-Host "=============================================" -ForegroundColor Green
} else {
    Write-Host "=============================================" -ForegroundColor Yellow
    Write-Host "  INSTALLATION COMPLETE (with warnings)" -ForegroundColor Yellow
    Write-Host "=============================================" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "Installed to:" -ForegroundColor Cyan
Write-Host "  ~/.gemini/     - Gemini CLI configuration"
Write-Host "  ~/.claude/     - Claude Code configuration"
Write-Host "  ~/.codex/      - Codex CLI configuration"
Write-Host ""
Write-Host "Test with:" -ForegroundColor Yellow
Write-Host "  gemini 'Hello, test the configuration'"
Write-Host "  gemini -e code-analyst 'List available agents'"
Write-Host "  codex exec 'Hello, test Codex configuration'"
Write-Host ""
