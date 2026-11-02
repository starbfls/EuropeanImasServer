# Always use the project's Python, regardless of the terminal's active environment.
$ErrorActionPreference = 'Stop'
$projectPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (!(Test-Path -LiteralPath $projectPython -PathType Leaf)) {
    throw 'Missing backend/.venv. In backend, run: python -m venv .venv, then .\.venv\Scripts\python.exe -m pip install -r requirements.txt'
}

& $projectPython -X utf8 (Join-Path $PSScriptRoot 'app.py')
exit $LASTEXITCODE
