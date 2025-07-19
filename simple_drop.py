import sqlite3
import sys

def main():
    db_path = r"c:\DEV\APP_ATARYS V2\data\atarys_data.db"
    
    try:
        # Se connecter à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_cle';")
        if cursor.fetchone():
            print("Table 'test_cle' trouvée. Suppression en cours...")
            
            # Désactiver les contraintes de clé étrangère
            cursor.execute("PRAGMA foreign_keys = OFF;")
            
            # Supprimer la table
            cursor.execute("DROP TABLE IF EXISTS test_cle;")
            
            # Réactiver les contraintes de clé étrangère
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            # Valider les changements
            conn.commit()
            print("✅ La table 'test_cle' a été supprimée avec succès.")
        else:
            print("La table 'test_cle' n'existe pas dans la base de données.")
            
        # Afficher la liste des tables restantes
        print("\nTables restantes dans la base de données:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if tables:
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("Aucune table trouvée.")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== Suppression de la table 'test_cle' ===\n")
    main()
    input("\nAppuyez sur Entrée pour quitter...")
