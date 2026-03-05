param(
    [switch]$apply,
    [switch]$dryRun,
    [switch]$force,
    [switch]$reinit,
    [string]$projectRoot = ".",
    [string]$sourceDocs = ""
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "init_spec_repo.py"

$args = @("--project-root", $projectRoot)
if ($sourceDocs -ne "") {
    $args += @("--source-docs", $sourceDocs)
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

python $pythonScript @args
exit $LASTEXITCODE
