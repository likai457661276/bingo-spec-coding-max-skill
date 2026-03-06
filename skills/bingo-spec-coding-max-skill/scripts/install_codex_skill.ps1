param(
    [ValidateSet("symlink", "copy")]
    [string]$Mode = "copy",
    [string]$CodexHome = "",
    [switch]$Force
)

if ([string]::IsNullOrWhiteSpace($CodexHome)) {
    $CodexHome = $env:CODEX_HOME
}

if ([string]::IsNullOrWhiteSpace($CodexHome)) {
    $CodexHome = Join-Path $HOME ".codex"
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillSourceDir = Split-Path -Parent $scriptDir
$targetRoot = Join-Path $CodexHome "skills"
$targetDir = Join-Path $targetRoot "bingo-spec-coding-max-skill"

New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null

if (Test-Path $targetDir) {
    if (-not $Force) {
        Write-Error "Target already exists: $targetDir . Re-run with -Force to replace it."
        exit 1
    }
    Remove-Item -Recurse -Force $targetDir
}

if ($Mode -eq "symlink") {
    New-Item -ItemType SymbolicLink -Path $targetDir -Target $skillSourceDir | Out-Null
    $action = "symlinked"
}
else {
    Copy-Item -Recurse -Force $skillSourceDir $targetDir
    $action = "copied"
}

Write-Output "[OK] Skill $action to: $targetDir"
Write-Output "[INFO] Using CODEX_HOME: $CodexHome"
Write-Output "[INFO] Trigger from a target project with: `$bingo-spec-coding-max-skill"
