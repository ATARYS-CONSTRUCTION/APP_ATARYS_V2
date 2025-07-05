# ATARYS V2 - Script de Sauvegarde Automatique
# Sauvegarde automatique vers GitHub avec horodatage

param(
    [string]$Message = "Sauvegarde automatique - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    [switch]$Force = $false
)

# Configuration
$ProjectPath = "C:\DEV\APP_ATARYS V2"
$LogFile = "$ProjectPath\logs\sauvegarde.log"
$BackupPath = "C:\DEV\SAUVEGARDES\ATARYS_V2"

# Fonction de logging
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    Write-Host $LogEntry
    Add-Content -Path $LogFile -Value $LogEntry
}

# Créer le dossier de logs s'il n'existe pas
if (-not (Test-Path "$ProjectPath\logs")) {
    New-Item -ItemType Directory -Path "$ProjectPath\logs" -Force
}

Write-Log "=== DÉBUT SAUVEGARDE AUTOMATIQUE ATARYS V2 ==="

try {
    # Vérifier si on est dans le bon répertoire
    Set-Location $ProjectPath
    Write-Log "Répertoire de travail : $ProjectPath"

    # Vérifier le statut Git
    $GitStatus = git status --porcelain
    if (-not $GitStatus -and -not $Force) {
        Write-Log "Aucun changement détecté. Utiliser -Force pour forcer la sauvegarde." "WARNING"
        return
    }

    # Ajouter tous les fichiers modifiés
    Write-Log "Ajout des fichiers modifiés..."
    git add .
    
    # Créer le commit
    Write-Log "Création du commit : $Message"
    git commit -m $Message
    
    # Pousser vers GitHub
    Write-Log "Push vers GitHub..."
    git push origin main
    
    Write-Log "✅ Sauvegarde GitHub réussie !" "SUCCESS"

    # Sauvegarde locale supplémentaire
    if (Test-Path $BackupPath) {
        Write-Log "Création de la sauvegarde locale..."
        $BackupDate = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
        $BackupFolder = "$BackupPath\ATARYS_V2_$BackupDate"
        
        # Copier les fichiers importants (exclure .git, node_modules, etc.)
        robocopy $ProjectPath $BackupFolder /E /XD .git node_modules .vite dist __pycache__ /XF *.log *.tmp /R:3 /W:1 /MT:8 /LOG+:$LogFile
        
        Write-Log "✅ Sauvegarde locale créée : $BackupFolder" "SUCCESS"
    }

} catch {
    Write-Log "❌ Erreur lors de la sauvegarde : $($_.Exception.Message)" "ERROR"
    throw
}

Write-Log "=== FIN SAUVEGARDE AUTOMATIQUE ===" 