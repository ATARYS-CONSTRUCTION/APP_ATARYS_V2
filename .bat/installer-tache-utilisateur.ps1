# ATARYS V2 - Installation Tâche Utilisateur (sans admin)
# Installe la tâche planifiée pour l'utilisateur courant

$TaskName = "ATARYS_V2_Sauvegarde_Auto"
$ScriptPath = "C:\DEV\APP_ATARYS V2\.bat\sauvegarde-auto.ps1"
$WorkingDirectory = "C:\DEV\APP_ATARYS V2"

Write-Host "=== Installation Sauvegarde Quotidienne 21h (Utilisateur) ===" -ForegroundColor Green

try {
    # Supprimer la tâche existante si elle existe
    try {
        $ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction Stop
        Write-Host "Suppression de la tâche existante..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    } catch {
        Write-Host "Aucune tâche existante trouvée." -ForegroundColor Gray
    }

    # Créer l'action
    $Action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$ScriptPath`"" -WorkingDirectory $WorkingDirectory

    # Créer UNIQUEMENT le déclencheur quotidien à 21h
    $Trigger = New-ScheduledTaskTrigger -Daily -At "21:00"

    # Créer les paramètres (sans RunOnlyIfNetworkAvailable qui nécessite admin)
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

    # Créer le principal pour l'utilisateur courant (pas besoin d'admin)
    $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

    # Enregistrer la tâche
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "Sauvegarde automatique quotidienne du projet ATARYS V2 à 21h"

    Write-Host "✅ Tâche planifiée créée avec succès !" -ForegroundColor Green
    Write-Host ""
    Write-Host "Configuration :" -ForegroundColor Cyan
    Write-Host "  • Sauvegarde quotidienne à 21h00" -ForegroundColor Green
    Write-Host "  • Pas de sauvegarde automatique toutes les 2h" -ForegroundColor Yellow
    Write-Host "  • Utilisateur : $env:USERNAME" -ForegroundColor White
    Write-Host ""
    
    # Vérifier que la tâche a été créée
    $CreatedTask = Get-ScheduledTask -TaskName $TaskName
    Write-Host "Tâche créée : $($CreatedTask.TaskName)" -ForegroundColor Green
    Write-Host "État : $($CreatedTask.State)" -ForegroundColor Green
    
    # Afficher les détails du déclencheur
    $TaskTrigger = Get-ScheduledTaskTrigger -TaskName $TaskName
    Write-Host "Déclencheur : Quotidien à $($TaskTrigger.StartBoundary.ToString('HH:mm'))" -ForegroundColor Green

} catch {
    Write-Host "❌ Erreur lors de la création de la tâche : $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Pour voir la tâche : Gestionnaire des tâches > Bibliothèque du Planificateur de tâches" -ForegroundColor Yellow
Write-Host ""
Write-Host "Appuyez sur une touche pour continuer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 