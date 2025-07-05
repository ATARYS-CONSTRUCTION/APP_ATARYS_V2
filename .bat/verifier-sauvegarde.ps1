# ATARYS V2 - Vérification Sauvegarde Automatique
# Script pour vérifier l'état de la sauvegarde automatique

$TaskName = "ATARYS_V2_Sauvegarde_Auto"

Write-Host "=== Vérification Sauvegarde Automatique ATARYS V2 ===" -ForegroundColor Green
Write-Host ""

try {
    # Vérifier si la tâche existe
    $Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction Stop
    
    Write-Host "✅ Tâche planifiée trouvée !" -ForegroundColor Green
    Write-Host "Nom : $($Task.TaskName)" -ForegroundColor White
    Write-Host "État : $($Task.State)" -ForegroundColor White
    Write-Host "Description : $($Task.Description)" -ForegroundColor White
    Write-Host ""
    
    # Vérifier les déclencheurs
    Write-Host "Déclencheurs configurés :" -ForegroundColor Cyan
    $Triggers = Get-ScheduledTaskTrigger -TaskName $TaskName
    
    foreach ($Trigger in $Triggers) {
        if ($Trigger.CimClass.CimClassName -eq "MSFT_TaskDailyTrigger") {
            $Time = [DateTime]::Parse($Trigger.StartBoundary).ToString("HH:mm")
            Write-Host "  • Sauvegarde quotidienne à $Time" -ForegroundColor Green
        }
        elseif ($Trigger.CimClass.CimClassName -eq "MSFT_TaskSessionStateChangeTrigger") {
            Write-Host "  • Sauvegarde à la fermeture de session" -ForegroundColor Yellow
        }
        elseif ($Trigger.CimClass.CimClassName -eq "MSFT_TaskTimeTrigger") {
            if ($Trigger.Repetition.Interval) {
                Write-Host "  • Sauvegarde répétée (SUPPRIMÉE)" -ForegroundColor Red
            }
        }
    }
    
    # Vérifier les informations d'exécution
    Write-Host ""
    Write-Host "Informations d'exécution :" -ForegroundColor Cyan
    $TaskInfo = Get-ScheduledTaskInfo -TaskName $TaskName
    Write-Host "  • Dernière exécution : $($TaskInfo.LastRunTime)" -ForegroundColor White
    Write-Host "  • Prochaine exécution : $($TaskInfo.NextRunTime)" -ForegroundColor White
    Write-Host "  • Résultat dernière exécution : $($TaskInfo.LastTaskResult)" -ForegroundColor White
    
    # Vérifier les fichiers
    Write-Host ""
    Write-Host "Vérification des fichiers :" -ForegroundColor Cyan
    
    $ScriptPath = "C:\DEV\APP_ATARYS V2\.bat\sauvegarde-auto.ps1"
    if (Test-Path $ScriptPath) {
        Write-Host "  ✅ Script de sauvegarde trouvé" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Script de sauvegarde introuvable" -ForegroundColor Red
    }
    
    $LogPath = "C:\DEV\APP_ATARYS V2\logs\sauvegarde.log"
    if (Test-Path $LogPath) {
        Write-Host "  ✅ Fichier de log trouvé" -ForegroundColor Green
        $LogSize = (Get-Item $LogPath).Length
        Write-Host "    Taille : $([math]::Round($LogSize/1KB, 2)) KB" -ForegroundColor Gray
    } else {
        Write-Host "  ⚠️ Fichier de log non trouvé (normal si première utilisation)" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ Tâche planifiée introuvable !" -ForegroundColor Red
    Write-Host "Utilisez le script 'installer-sauvegarde-21h-simple.ps1' pour l'installer." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Test Manuel ===" -ForegroundColor Green
Write-Host "Pour tester la sauvegarde manuellement :" -ForegroundColor White
Write-Host "  .\.bat\sauvegarde-auto.ps1 -Force" -ForegroundColor Cyan
Write-Host ""
Write-Host "Appuyez sur une touche pour continuer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 