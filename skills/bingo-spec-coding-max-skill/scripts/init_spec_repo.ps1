param(
    [switch]$apply,
    [switch]$dryRun,
    [switch]$force,
    [switch]$reinit,
    [switch]$upgrade,
    [string]$projectRoot = ".",
    [string]$sourceDocs = "",
    [ValidateSet("zh", "en")]
    [string]$language = "zh"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "init_spec_repo.py"

$args = @("--project-root", $projectRoot)
if ($sourceDocs -ne "") {
    $args += @("--source-docs", $sourceDocs)
}
if ($language -ne "") {
    $args += @("--language", $language)
}
if ($apply) {
    $args += "--apply"
}
if ($dryRun) {
    $args += "--dry-run"
}
if ($force) {
    $args += "--force"
}
if ($reinit) {
    $args += "--reinit"
}
if ($upgrade) {
    $args += "--upgrade"
}

python $pythonScript @args
exit $LASTEXITCODE
