# SBOM generation script for KOINZ
# Generates dependency SBOMs for backend (pip) and frontends (npm)
# Requires: syft installed (https://github.com/anchore/syft)

Write-Host "Generating KOINZ SBOM artifacts..."

if (Test-Path "backend\requirements.txt") {
    Write-Host "Backend SBOM..."
    & syft dir:./backend -o cyclonedx-json --file sbom-backend.json 2>$null
    if (-not $?) { Write-Warning "syft not found; skipping backend SBOM" }
}

if (Test-Path "web-app\package-lock.json") {
    Write-Host "Web-app SBOM..."
    & syft dir:./web-app -o cyclonedx-json --file sbom-web.json 2>$null
    if (-not $?) { Write-Warning "syft not found; skipping web SBOM" }
}

Write-Host "Done."