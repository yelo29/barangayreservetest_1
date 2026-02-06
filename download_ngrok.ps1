# Download and setup ngrok automatically
Write-Host "🚀 Downloading ngrok..." -ForegroundColor Green

# Create ngrok directory
New-Item -ItemType Directory -Force -Path "ngrok"

# Download ngrok
$url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
$output = "ngrok\ngrok.zip"
Invoke-WebRequest -Uri $url -OutFile $output

# Extract
Write-Host "📦 Extracting ngrok..." -ForegroundColor Green
Expand-Archive -Path "ngrok\ngrok.zip" -DestinationPath "ngrok" -Force

# Cleanup
Remove-Item "ngrok\ngrok.zip"

Write-Host "✅ Ngrok ready!" -ForegroundColor Green
Write-Host "🚀 Run: cd ngrok; .\ngrok.exe http 8080" -ForegroundColor Yellow
