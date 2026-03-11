param(
    [string]$TargetProject = ".",
    [switch]$Force,
    [switch]$Clean
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillDir = Split-Path -Parent $scriptDir
$sourceDocDir = Join-Path (Join-Path $skillDir "resources") "doc"
$targetProjectDir = (Resolve-Path $TargetProject).Path
$targetDocDir = Join-Path $targetProjectDir "doc"

if (-not (Test-Path $sourceDocDir)) {
    Write-Error "Bundled doc templates not found: $sourceDocDir"
    exit 1
}

if ($Clean -and (Test-Path $targetDocDir)) {
    Remove-Item -Recurse -Force $targetDocDir
    Write-Output "[REMOVE] Existing doc inputs cleared: $targetDocDir"
}

New-Item -ItemType Directory -Force -Path $targetDocDir | Out-Null

$sourceFiles = Get-ChildItem -Recurse -File $sourceDocDir
foreach ($sourceFile in $sourceFiles) {
    $relativePath = $sourceFile.FullName.Substring($sourceDocDir.Length).TrimStart('\', '/')
    $targetFile = Join-Path $targetDocDir $relativePath
    $targetParent = Split-Path -Parent $targetFile

    New-Item -ItemType Directory -Force -Path $targetParent | Out-Null

    if ((Test-Path $targetFile) -and (-not $Force)) {
        Write-Error "Target file already exists: $targetFile . Re-run with -Force to overwrite existing doc inputs."
        exit 1
    }

    Copy-Item -Force $sourceFile.FullName $targetFile
    Write-Output "[COPY ] $targetFile"
}

Write-Output "[OK] Target project prepared: $targetProjectDir"
Write-Output "[INFO] Next step: trigger `$bingo-spec-coding-max-skill inside the target project."
