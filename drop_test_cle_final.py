import sqlite3
from pathlib import Path

def drop_test_cle():
    # Chemin vers la base de données
    db_path = Path(r"c:\DEV\APP_ATARYS V2\data\atarys_data.db")
    
    if not db_path.exists():
        print(f"Erreur: La base de données n'existe pas à l'emplacement: {db_path}")
        return
    
    print(f"Connexion à la base de données: {db_path}")
    
    try:
        # Se connecter à la base de données
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_cle';")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("\n=== Table 'test_cle' trouvée ===")
            
            # Afficher la structure de la table
            print("\nStructure de la table 'test_cle':")
            cursor.execute("PRAGMA table_info(test_cle);")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  - {col[1]}: {col[2]}")
            
            # Afficher les premières lignes
            print("\nContenu de la table (5 premières lignes):")
            cursor.execute("SELECT * FROM test_cle LIMIT 5;")
            rows = cursor.fetchall()
            if rows:
                # Afficher les noms des colonnes
                col_names = [description[0] for description in cursor.description]
                print("  " + " | ".join(col_names))
                print("  " + "-" * 50)
                
                # Afficher les données
                for row in rows:
                    print("  " + " | ".join(str(value) for value in row))
            else:
                print("  La table est vide.")
            
            # Demander confirmation
            confirm = input("\nVoulez-vous vraiment supprimer cette table ? (o/n): ")
            if confirm.lower() != 'o':
                print("Opération annulée.")
                return
            
            # Désactiver temporairement les contraintes de clé étrangère
            cursor.execute("PRAGMA foreign_keys = OFF;")
            
            # Supprimer la table
            cursor.execute("DROP TABLE IF EXISTS test_cle;")
            
            # Réactiver les contraintes de clé étrangère
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            # Valider les changements
            conn.commit()
            print("\n✅ La table 'test_cle' a été supprimée avec succès.")
            
        else:
            print("\nLa table 'test_cle' n'existe pas dans la base de données.")
        
        # Afficher la liste des tables restantes
        print("\n=== Liste des tables dans la base de données ===")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if tables:
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("Aucune table trouvée dans la base de données.")
            
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== Script de suppression de la table 'test_cle' ===\n")
    drop_test_cle()
    input("\nAppuyez sur Entrée pour quitter...")
