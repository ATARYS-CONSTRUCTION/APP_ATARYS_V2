import os
import shutil
import subprocess
from pathlib import Path

def reset_migrations():
    # Chemin du dossier backend
    backend_dir = Path(__file__).parent / 'backend'
    
    # Se placer dans le dossier backend
    os.chdir(backend_dir)
    
    # 1. Supprimer le dossier de migrations s'il existe
    migrations_dir = backend_dir / 'migrations'
    if migrations_dir.exists():
        print("Suppression du dossier de migrations existant...")
        shutil.rmtree(migrations_dir)
    
    # 2. Initialiser Alembic
    print("\nInitialisation d'Alembic...")
    subprocess.run(["python", "-m", "flask", "db", "init"], check=True)
    
    # 3. Créer une migration initiale
    print("\nCréation de la migration initiale...")
    subprocess.run(["python", "-m", "flask", "db", "migrate", "-m", "Initial migration"], check=True)
    
    # 4. Appliquer les migrations
    print("\nApplication des migrations...")
    subprocess.run(["python", "-m", "flask", "db", "upgrade"], check=True)
    
    print("\n✅ Réinitialisation des migrations terminée avec succès !")

if __name__ == "__main__":
    print("=== Réinitialisation complète des migrations ===\n")
    try:
        reset_migrations()
    except Exception as e:
        print(f"\n❌ Erreur lors de la réinitialisation : {e}")
    
    input("\nAppuyez sur Entrée pour quitter...")
