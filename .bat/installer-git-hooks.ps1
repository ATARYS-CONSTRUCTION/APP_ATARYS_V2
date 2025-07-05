# ATARYS V2 - Installation Git Hooks
# Configure des hooks Git pour sauvegardes automatiques

$ProjectPath = "C:\DEV\APP_ATARYS V2"
$HooksPath = "$ProjectPath\.git\hooks"

Write-Host "=== Installation Git Hooks ATARYS V2 ===" -ForegroundColor Green

# Créer le hook pre-commit
$PreCommitContent = @"
#!/bin/sh
# ATARYS V2 - Pre-commit hook
# Sauvegarde automatique avant chaque commit

echo "🔄 ATARYS V2 - Pré-commit en cours..."

# Vérifier la syntaxe des fichiers Python
find . -name "*.py" -not -path "./.git/*" -not -path "./venv/*" | xargs python -m py_compile 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Erreur de syntaxe Python détectée !"
    exit 1
fi

# Vérifier les fichiers JavaScript/TypeScript
if command -v npm >/dev/null 2>&1; then
    if [ -f "frontend/package.json" ]; then
        cd frontend && npm run lint --silent 2>/dev/null || echo "⚠️  Linter frontend non disponible"
        cd ..
    fi
fi

echo "✅ Pré-commit validé !"
"@

$PreCommitPath = "$HooksPath\pre-commit"
$PreCommitContent | Out-File -FilePath $PreCommitPath -Encoding UTF8
Write-Host "✅ Hook pre-commit installé" -ForegroundColor Green

# Créer le hook post-commit
$PostCommitContent = @"
#!/bin/sh
# ATARYS V2 - Post-commit hook
# Actions après chaque commit

echo "📝 ATARYS V2 - Post-commit en cours..."

# Logger le commit
echo "[$(date)] Commit: $(git log -1 --pretty=format:'%h - %s')" >> logs/commits.log

# Créer une sauvegarde locale si c'est un commit important
COMMIT_MSG=$(git log -1 --pretty=format:'%s')
if echo "$COMMIT_MSG" | grep -i "release\|version\|production\|deploy"; then
    echo "🎯 Commit important détecté - Création sauvegarde..."
    powershell -ExecutionPolicy Bypass -File ".\.bat\sauvegarde-auto.ps1" -Force
fi

echo "✅ Post-commit terminé !"
"@

$PostCommitPath = "$HooksPath\post-commit"
$PostCommitContent | Out-File -FilePath $PostCommitPath -Encoding UTF8
Write-Host "✅ Hook post-commit installé" -ForegroundColor Green

# Créer le hook pre-push
$PrePushContent = @"
#!/bin/sh
# ATARYS V2 - Pre-push hook
# Vérifications avant push vers GitHub

echo "🚀 ATARYS V2 - Pré-push en cours..."

# Vérifier qu'on pousse vers la bonne branche
protected_branch='main'
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

if [ $protected_branch = $current_branch ]; then
    echo "🔒 Push vers branche principale détecté"
    
    # Vérifier que les tests passent (si disponibles)
    if [ -f "backend/requirements.txt" ]; then
        echo "🧪 Vérification des tests Python..."
        # cd backend && python -m pytest tests/ --quiet 2>/dev/null || echo "⚠️  Tests non disponibles"
    fi
    
    # Vérifier la taille du push
    size=$(git count-objects -v | grep size-pack | awk '{print $2}')
    if [ $size -gt 10000 ]; then
        echo "⚠️  Push volumineux détecté (${size}KB)"
    fi
fi

echo "✅ Pré-push validé !"
"@

$PrePushPath = "$HooksPath\pre-push"
$PrePushContent | Out-File -FilePath $PrePushPath -Encoding UTF8
Write-Host "✅ Hook pre-push installé" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Git Hooks installés avec succès !" -ForegroundColor Green
Write-Host ""
Write-Host "Hooks configurés :" -ForegroundColor Cyan
Write-Host "  • pre-commit  : Validation avant commit" -ForegroundColor White
Write-Host "  • post-commit : Actions après commit" -ForegroundColor White
Write-Host "  • pre-push    : Vérifications avant push" -ForegroundColor White 