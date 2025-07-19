import os
import shutil
import sqlite3
from pathlib import Path

def reset_database():
    print("=== Réinitialisation de la base de données ===\n")
    
    # Chemins importants
    base_dir = Path(__file__).parent
    db_path = base_dir / 'data' / 'atarys_data.db'
    migrations_dir = base_dir / 'backend' / 'migrations'
    
    # 1. Sauvegarder l'ancienne base de données
    backup_path = str(db_path) + '.backup'
    if db_path.exists():
        print(f"Sauvegarde de la base de données dans {backup_path}")
        try:
            if os.path.exists(backup_path):
                os.remove(backup_path)
            shutil.copy2(db_path, backup_path)
            print("✅ Sauvegarde effectuée")
        except Exception as e:
            print(f"⚠️ Impossible de sauvegarder la base de données : {e}")
    
    # 2. Supprimer la base de données existante
    if db_path.exists():
        print("\nSuppression de l'ancienne base de données...")
        try:
            os.remove(db_path)
            print("✅ Ancienne base de données supprimée")
        except Exception as e:
            print(f"⚠️ Impossible de supprimer la base de données : {e}")
    
    # 3. Supprimer le dossier de migrations
    if migrations_dir.exists():
        print("\nSuppression de l'ancien dossier de migrations...")
        try:
            shutil.rmtree(migrations_dir)
            print("✅ Ancien dossier de migrations supprimé")
        except Exception as e:
            print(f"⚠️ Impossible de supprimer le dossier de migrations : {e}")
    
    print("\n=== Réinitialisation terminée ===")
    print("\nVeuillez maintenant exécuter les commandes suivantes dans l'ordre :")
    print("1. cd backend")
    print("2. python -m flask db init")
    print("3. python -m flask db migrate -m 'Initial migration'")
    print("4. python -m flask db upgrade")
    print("\nCela créera une nouvelle base de données vide avec les tables nécessaires.")

if __name__ == "__main__":
    reset_database()
    input("\nAppuyez sur Entrée pour quitter...")
