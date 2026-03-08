param(
    [string]$TargetProject = ".",
    [ValidateSet("symlink", "copy")]
    [string]$Mode = "copy",
    [string]$CodexHome = "",
    [switch]$Force,
    [switch]$UpgradeSkill
)

if ([string]::IsNullOrWhiteSpace($CodexHome)) {
    $CodexHome = $env:CODEX_HOME
}

if ([string]::IsNullOrWhiteSpace($CodexHome)) {
    $CodexHome = Join-Path $HOME ".codex"
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$resolvedTargetProject = (Resolve-Path $TargetProject).Path
$targetDocDir = Join-Path $resolvedTargetProject "doc"
$skillTargetDir = Join-Path (Join-Path $CodexHome "skills") "bingo-spec-coding-max-skill"
$replaceSkill = $Force -or $UpgradeSkill
$docFilesExist = $false

if (Test-Path $targetDocDir) {
    $docFilesExist = $null -ne (Get-ChildItem -Path $targetDocDir -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 1)
}

$installArgs = @{
    Mode = $Mode
    CodexHome = $CodexHome
}

$prepareArgs = @{
    TargetProject = $TargetProject
}

if ($Force) {
    $installArgs["Force"] = $true
    $prepareArgs["Force"] = $true
}
if ($UpgradeSkill) {
    $installArgs["Upgrade"] = $true
}

if ((Test-Path $skillTargetDir) -and (-not $replaceSkill)) {
    Write-Output "[SKIP ] Existing Codex skill preserved: $skillTargetDir"
}
else {
    & (Join-Path $scriptDir "install_codex_skill.ps1") @installArgs
    if (-not $?) {
        exit 1
    }
}

if ((-not $Force) -and $docFilesExist) {
    Write-Output "[SKIP ] Existing doc inputs preserved: $targetDocDir"
}
else {
    & (Join-Path $scriptDir "prepare_target_project.ps1") @prepareArgs
    if (-not $?) {
        exit 1
    }
}

Write-Output "[OK] Codex skill installed and target project prepared."
Write-Output "[INFO] Open the target project in Codex and trigger: `$bingo-spec-coding-max-skill"
