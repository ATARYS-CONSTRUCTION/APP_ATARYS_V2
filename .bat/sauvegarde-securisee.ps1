# ATARYS V2 - Script de Sauvegarde SÉCURISÉ
# Version corrigée qui ne supprime JAMAIS rien !

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

# SÉCURITÉ : Vérifier que nous sommes dans le bon répertoire
if (-not (Test-Path "$ProjectPath\.git")) {
    Write-Log "❌ ERREUR : Pas dans un dépôt Git valide ! Arrêt pour sécurité." "ERROR"
    throw "Répertoire de travail incorrect"
}

# Créer le dossier de logs s'il n'existe pas
if (-not (Test-Path "$ProjectPath\logs")) {
    New-Item -ItemType Directory -Path "$ProjectPath\logs" -Force
}

Write-Log "=== DÉBUT SAUVEGARDE SÉCURISÉE ATARYS V2 ==="

try {
    # Vérifier si on est dans le bon répertoire
    Set-Location $ProjectPath
    Write-Log "Répertoire de travail : $ProjectPath"

    # SÉCURITÉ : Vérifier les fichiers critiques
    $FichiersCritiques = @("package.json", "vite.config.js", "index.html")
    foreach ($fichier in $FichiersCritiques) {
        $CheminFichier = Join-Path "frontend" $fichier
        if (Test-Path $CheminFichier) {
            Write-Log "✅ Fichier critique trouvé : $CheminFichier"
        } else {
            Write-Log "⚠️ Fichier critique manquant : $CheminFichier" "WARNING"
        }
    }

    # Vérifier le statut Git
    $GitStatus = git status --porcelain
    if (-not $GitStatus -and -not $Force) {
        Write-Log "Aucun changement détecté. Utiliser -Force pour forcer la sauvegarde." "WARNING"
        return
    }

    # SÉCURITÉ : Afficher ce qui va être ajouté
    Write-Log "Fichiers à ajouter :"
    git status --porcelain | ForEach-Object { Write-Log "  $_" }

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

    # Sauvegarde locale ULTRA-SÉCURISÉE
    if (Test-Path $BackupPath) {
        Write-Log "Création de la sauvegarde locale SÉCURISÉE..."
        $BackupDate = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
        $BackupFolder = "$BackupPath\ATARYS_V2_$BackupDate"
        
        # Créer le dossier de destination
        New-Item -ItemType Directory -Path $BackupFolder -Force
        
        # SÉCURITÉ : Copie explicite par dossier (pas de robocopy global)
        Write-Log "Copie sécurisée des dossiers..."
        
        # Copier les dossiers importants un par un
        $DossiersACopier = @("docs", "backend", "frontend", "data")
        foreach ($dossier in $DossiersACopier) {
            if (Test-Path $dossier) {
                Write-Log "Copie du dossier : $dossier"
                robocopy "$ProjectPath\$dossier" "$BackupFolder\$dossier" /E /R:3 /W:1
            }
        }
        
        # Copier les fichiers racine importants
        $FichiersRacine = @(".cursorrules", ".gitignore", "README.md")
        foreach ($fichier in $FichiersRacine) {
            if (Test-Path $fichier) {
                Write-Log "Copie du fichier : $fichier"
                Copy-Item $fichier $BackupFolder
            }
        }
        
        Write-Log "✅ Sauvegarde locale sécurisée créée : $BackupFolder" "SUCCESS"
    }

} catch {
    Write-Log "❌ Erreur lors de la sauvegarde : $($_.Exception.Message)" "ERROR"
    throw
}

Write-Log "=== FIN SAUVEGARDE SÉCURISÉE ===" 