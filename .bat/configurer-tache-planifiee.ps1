# ATARYS V2 - Configuration Tâche Planifiée
# Configure une tâche Windows pour sauvegardes automatiques

# Vérifier les droits administrateur
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Ce script nécessite des droits administrateur." -ForegroundColor Red
    Write-Host "Relancez PowerShell en tant qu'administrateur." -ForegroundColor Yellow
    pause
    exit 1
}

# Configuration de la tâche
$TaskName = "ATARYS_V2_Sauvegarde_Auto"
$ScriptPath = "C:\DEV\APP_ATARYS V2\.bat\sauvegarde-auto.ps1"
$WorkingDirectory = "C:\DEV\APP_ATARYS V2"

Write-Host "=== Configuration Tâche Planifiée ATARYS V2 ===" -ForegroundColor Green

try {
    # Supprimer la tâche existante si elle existe
    $ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($ExistingTask) {
        Write-Host "Suppression de la tâche existante..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }

    # Créer l'action
    $Action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$ScriptPath`"" -WorkingDirectory $WorkingDirectory

    # Créer les déclencheurs
    $Triggers = @()
    
    # Déclencheur 1 : Tous les jours à 18h00
    $Triggers += New-ScheduledTaskTrigger -Daily -At "18:00"
    
    # Déclencheur 2 : À la fermeture de session
    $Triggers += New-ScheduledTaskTrigger -AtLogOff
    
    # Déclencheur 3 : Toutes les 2 heures pendant les heures de travail
    $Triggers += New-ScheduledTaskTrigger -Once -At "08:00" -RepetitionInterval (New-TimeSpan -Hours 2) -RepetitionDuration (New-TimeSpan -Hours 10)

    # Créer les paramètres
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

    # Créer le principal (utilisateur actuel)
    $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

    # Enregistrer la tâche
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Triggers -Settings $Settings -Principal $Principal -Description "Sauvegarde automatique du projet ATARYS V2 vers GitHub"

    Write-Host "✅ Tâche planifiée créée avec succès !" -ForegroundColor Green
    Write-Host ""
    Write-Host "Déclencheurs configurés :" -ForegroundColor Cyan
    Write-Host "  • Tous les jours à 18h00" -ForegroundColor White
    Write-Host "  • À la fermeture de session" -ForegroundColor White
    Write-Host "  • Toutes les 2 heures (8h-18h)" -ForegroundColor White
    Write-Host ""
    Write-Host "Pour voir la tâche : Gestionnaire des tâches > Bibliothèque du Planificateur de tâches" -ForegroundColor Yellow

} catch {
    Write-Host "❌ Erreur lors de la création de la tâche : $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Appuyez sur une touche pour continuer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 