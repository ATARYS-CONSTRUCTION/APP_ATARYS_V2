import sqlite3

def check_alembic_version():
    db_path = r"c:\DEV\APP_ATARYS V2\data\atarys_data.db"
    
    try:
        # Se connecter à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si la table alembic_version existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alembic_version';")
        if not cursor.fetchone():
            print("La table 'alembic_version' n'existe pas dans la base de données.")
            return
        
        # Afficher le contenu de la table alembic_version
        cursor.execute("SELECT * FROM alembic_version;")
        version = cursor.fetchone()
        
        if version:
            print(f"Version actuelle d'Alembic dans la base de données: {version[0]}")
        else:
            print("La table 'alembic_version' est vide.")
        
        # Vérifier si cette version existe dans les fichiers de migration
        import os
        migrations_dir = r"c:\DEV\APP_ATARYS V2\backend\migrations\versions"
        version_found = False
        
        if os.path.exists(migrations_dir):
            for filename in os.listdir(migrations_dir):
                if filename.endswith('.py') and version and version[0] in filename:
                    print(f"\nFichier de migration correspondant trouvé: {filename}")
                    version_found = True
                    break
            
            if not version_found and version:
                print(f"\n⚠️ Aucun fichier de migration trouvé pour la version: {version[0]}")
                print("C'est probablement la cause du problème de migration.")
        
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== Vérification de la version d'Alembic ===\n")
    check_alembic_version()
    input("\nAppuyez sur Entrée pour quitter...")
