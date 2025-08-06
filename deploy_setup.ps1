# RantSmith AI - Clean Deployment Setup Script
# This script creates a deployment-ready version without test files

Write-Host "🚀 Setting up clean RantSmith AI deployment..." -ForegroundColor Green

# Create new directory for clean deployment
$deployDir = "C:\Users\ASUS\Documents\GitHub\RantSmith-Deploy"
Write-Host "📁 Creating deployment directory: $deployDir" -ForegroundColor Cyan

if (Test-Path $deployDir) {
    Write-Host "⚠️  Deployment directory exists. Removing..." -ForegroundColor Yellow
    Remove-Item $deployDir -Recurse -Force
}

New-Item -ItemType Directory -Path $deployDir | Out-Null

# Copy essential files and directories
Write-Host "📂 Copying project files..." -ForegroundColor Cyan

# Core application files
Copy-Item "app" $deployDir -Recurse
Copy-Item "frontend" $deployDir -Recurse
Copy-Item "instance" $deployDir -Recurse

# Configuration files
Copy-Item "config.py" $deployDir
Copy-Item "run.py" $deployDir
Copy-Item "setup.py" $deployDir
Copy-Item "requirements.txt" $deployDir
Copy-Item "render.yaml" $deployDir
Copy-Item "Procfile" $deployDir

# Database setup
Copy-Item "create_db.py" $deployDir
Copy-Item "update_db.py" $deployDir
Copy-Item "final_validation.py" $deployDir

# Documentation
Copy-Item "README.md" $deployDir
Copy-Item "DEPLOY_GUIDE.md" $deployDir
Copy-Item "AI_CHAT_INTEGRATION_COMPLETE.md" $deployDir

# Environment template (without actual keys)
Write-Host "🔐 Creating environment template..." -ForegroundColor Cyan
$envTemplate = @"
# Environment Variables Template
# Copy this file to .env and fill in your actual values

# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
DEBUG=false

# Database Configuration
DATABASE_URL=sqlite:///rantsmith.db

# AI Service API Keys
GEMINI_API_KEY=your-gemini-api-key-here
ELEVENLABS_API_KEY=your-elevenlabs-api-key-here
RUNWAYML_API_KEY=your-runwayml-api-key-here

# Server Settings
HOST=0.0.0.0
PORT=5000
"@
$envTemplate | Out-File (Join-Path $deployDir ".env.template") -Encoding UTF8

# Create .gitignore for deployment
Write-Host "📝 Creating deployment .gitignore..." -ForegroundColor Cyan
$gitignoreContent = @"
# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Database
*.db
instance/

# Python
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Node modules
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
frontend/dist/
frontend/build/

# Uploads
uploads/
temp/
"@
$gitignoreContent | Out-File (Join-Path $deployDir ".gitignore") -Encoding UTF8

# Clean up __pycache__ directories
Write-Host "🧹 Cleaning Python cache files..." -ForegroundColor Cyan
Get-ChildItem $deployDir -Recurse -Name "__pycache__" -Force | ForEach-Object {
    $path = Join-Path $deployDir $_
    if (Test-Path $path) {
        Remove-Item $path -Recurse -Force
    }
}

# Initialize git repository
Write-Host "🔧 Initializing Git repository..." -ForegroundColor Cyan
Set-Location $deployDir
git init
git add .
git commit -m "Initial deployment-ready commit

Enhanced AI Chat with Psychologist Personality
Mood-uplifting responses and creative jokes
Production-ready configuration
Render and Vercel deployment ready
Clean codebase without test files

Features:
Professional psychologist AI (Dr. Elaichi)
Creative joke generation
Emotional support responses
Complete deployment setup"

Write-Host "✅ Deployment directory ready!" -ForegroundColor Green
Write-Host "📁 Location: $deployDir" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Next steps:" -ForegroundColor Yellow
Write-Host "1. Create new GitHub repository" -ForegroundColor White
Write-Host "2. Add remote: git remote add origin https://github.com/yourusername/rantsmith-ai.git" -ForegroundColor White
Write-Host "3. Push: git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Your clean RantSmith AI is ready for deployment!" -ForegroundColor Green
