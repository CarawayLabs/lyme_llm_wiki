# create_vscode_settings.ps1
#
# Creates:
#   .vscode/settings.json
#
# Run from the root directory of the repository:
#   .\create_vscode_settings.ps1
#
# To replace an existing settings.json:
#   .\create_vscode_settings.ps1 -Force

[CmdletBinding()]
param(
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepositoryRoot = (Get-Location).Path
$VsCodeDirectory = Join-Path -Path $RepositoryRoot -ChildPath ".vscode"
$SettingsPath = Join-Path -Path $VsCodeDirectory -ChildPath "settings.json"

$SettingsContent = @'
{
  "editor.formatOnSave": true,
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,

  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  },

  "[markdown]": {
    "editor.wordWrap": "on",
    "editor.quickSuggestions": {
      "comments": "off",
      "strings": "off",
      "other": "off"
    }
  },

  "python.analysis.typeCheckingMode": "basic"
}
'@

Write-Host ""
Write-Host "Repository root:" -ForegroundColor Cyan
Write-Host "  $RepositoryRoot"
Write-Host ""

if (-not (Test-Path -LiteralPath $VsCodeDirectory)) {
    New-Item `
        -ItemType Directory `
        -Path $VsCodeDirectory `
        -Force | Out-Null

    Write-Host "[CREATED] .vscode" -ForegroundColor Green
}
else {
    Write-Host "[EXISTS]  .vscode" -ForegroundColor DarkGray
}

if ((Test-Path -LiteralPath $SettingsPath) -and -not $Force) {
    Write-Warning ".vscode\settings.json already exists and was not changed."
    Write-Host ""
    Write-Host "To overwrite it, run:" -ForegroundColor Yellow
    Write-Host "  .\create_vscode_settings.ps1 -Force"
    exit 0
}

if ((Test-Path -LiteralPath $SettingsPath) -and $Force) {
    $Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $BackupPath = "$SettingsPath.$Timestamp.backup"

    Copy-Item `
        -LiteralPath $SettingsPath `
        -Destination $BackupPath

    Write-Host "[BACKUP]  .vscode\settings.json.$Timestamp.backup" -ForegroundColor Yellow
}

Set-Content `
    -LiteralPath $SettingsPath `
    -Value $SettingsContent `
    -Encoding utf8

Write-Host "[CREATED] .vscode\settings.json" -ForegroundColor Green
Write-Host ""
Write-Host "VS Code project settings are ready." -ForegroundColor Cyan