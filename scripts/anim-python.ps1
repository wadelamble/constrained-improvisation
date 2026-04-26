param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$PythonArgs
)

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$envRoot = Join-Path $scriptDir '..\.tools\micromamba-anim-root\envs\anim'
$envRoot = (Resolve-Path $envRoot).Path

$env:PATH = "$envRoot\Library\bin;$envRoot\Scripts;$envRoot;$env:PATH"

& "$envRoot\python.exe" @PythonArgs
$exitCode = $LASTEXITCODE
if ($null -eq $exitCode) {
    $exitCode = 0
}
exit $exitCode
