param(
    [string]$TargetProject = ".",
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

$installArgs = @("-Mode", $Mode, "-CodexHome", $CodexHome)
$prepareArgs = @("-TargetProject", $TargetProject)

if ($Force) {
    $installArgs += "-Force"
    $prepareArgs += "-Force"
}

& (Join-Path $scriptDir "install_codex_skill.ps1") @installArgs
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

& (Join-Path $scriptDir "prepare_target_project.ps1") @prepareArgs
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Output "[OK] Codex skill installed and target project prepared."
Write-Output "[INFO] Open the target project in Codex and trigger: `$bingo-spec-coding-max-skill"
