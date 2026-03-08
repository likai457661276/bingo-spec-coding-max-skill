param(
    [ValidateSet("symlink", "copy")]
    [string]$Mode = "copy",
    [string]$CodexHome = "",
    [switch]$Force,
    [switch]$Upgrade
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

$replaceExisting = $Force -or $Upgrade
$existingTarget = Test-Path $targetDir

if ($existingTarget) {
    if (-not $replaceExisting) {
        Write-Error "Target already exists: $targetDir . Re-run with -Force or -Upgrade to replace it."
        exit 1
    }
    Remove-Item -Recurse -Force $targetDir
}

if ($Mode -eq "symlink") {
    New-Item -ItemType SymbolicLink -Path $targetDir -Target $skillSourceDir | Out-Null
    $action = if ($existingTarget) { "upgraded via symlink" } else { "symlinked" }
}
else {
    Copy-Item -Recurse -Force $skillSourceDir $targetDir
    $action = if ($existingTarget) { "upgraded via copy" } else { "copied" }
}

Write-Output "[OK] Skill $action to: $targetDir"
Write-Output "[INFO] Using CODEX_HOME: $CodexHome"
Write-Output "[INFO] Trigger from a target project with: `$bingo-spec-coding-max-skill"
