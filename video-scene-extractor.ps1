$projectRoot = $PSScriptRoot
$uv = Get-Command uv.exe -ErrorAction SilentlyContinue

if ($uv) {
    & $uv.Source run --project $projectRoot video-scene-extractor @args
    return
}

$python = $null
$pythonArgs = @()
$environmentPythons = @(
    (Join-Path $projectRoot '.venv\Scripts\python.exe'),
    (Join-Path $projectRoot 'venv\Scripts\python.exe')
)

foreach ($candidate in $environmentPythons) {
    if (Test-Path -LiteralPath $candidate -PathType Leaf) {
        $python = $candidate
        break
    }
}

if (-not $python) {
    $pythonCommand = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($pythonCommand) {
        $python = $pythonCommand.Source
    } else {
        $pythonLauncher = Get-Command py.exe -ErrorAction SilentlyContinue
        if ($pythonLauncher) {
            $python = $pythonLauncher.Source
            $pythonArgs = @('-3')
        }
    }
}

if (-not $python) {
    [Console]::Error.WriteLine('Error: uv or Python 3.10+ was not found.')
    $global:LASTEXITCODE = 127
    return
}

& $python @pythonArgs -c 'import sys; raise SystemExit(sys.version_info < (3, 10))'
if ($LASTEXITCODE -ne 0) {
    [Console]::Error.WriteLine('Error: Python 3.10 or higher is required.')
    return
}

$sourceRoot = Join-Path $projectRoot 'src'
$pythonPathPreviouslySet = Test-Path Env:PYTHONPATH
$previousPythonPath = $env:PYTHONPATH
if ($previousPythonPath) {
    $env:PYTHONPATH = "$sourceRoot$([IO.Path]::PathSeparator)$previousPythonPath"
} else {
    $env:PYTHONPATH = $sourceRoot
}

& $python @pythonArgs -m video_scene_extractor @args
$pythonExitCode = $LASTEXITCODE
if ($pythonPathPreviouslySet) {
    $env:PYTHONPATH = $previousPythonPath
} else {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
$global:LASTEXITCODE = $pythonExitCode