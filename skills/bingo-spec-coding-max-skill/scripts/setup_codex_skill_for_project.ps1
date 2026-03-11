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

function Clear-TargetProjectRefreshState {
    param(
        [string]$ProjectDir
    )

    $docDir = Join-Path $ProjectDir "doc"
    $specDir = Join-Path $ProjectDir "spec"
    $agentsFile = Join-Path $ProjectDir "AGENTS.md"
    $lockFile = Join-Path $ProjectDir ".spec-bootstrap.lock"

    if (Test-Path $docDir) {
        Remove-Item -Recurse -Force $docDir
        Write-Output "[REMOVE] Existing doc inputs cleared: $docDir"
    }
    if (Test-Path $specDir) {
        Remove-Item -Recurse -Force $specDir
        Write-Output "[REMOVE] Existing spec directory cleared: $specDir"
    }
    if (Test-Path $agentsFile) {
        Remove-Item -Force $agentsFile
        Write-Output "[REMOVE] Existing AGENTS.md cleared: $agentsFile"
    }
    if (Test-Path $lockFile) {
        Remove-Item -Force $lockFile
        Write-Output "[REMOVE] Existing bootstrap lock cleared: $lockFile"
    }
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

if ($UpgradeSkill) {
    Clear-TargetProjectRefreshState -ProjectDir $resolvedTargetProject
    $prepareArgs["Clean"] = $true
    & (Join-Path $scriptDir "prepare_target_project.ps1") @prepareArgs
    if (-not $?) {
        exit 1
    }
    Write-Output "[INFO] Skill upgrade forces a full target-project refresh."
    Write-Output "[INFO] Re-run `$bingo-spec-coding-max-skill in the target project to regenerate the full spec system."
}
elseif ((-not $Force) -and $docFilesExist) {
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
