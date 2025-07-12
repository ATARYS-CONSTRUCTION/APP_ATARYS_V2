import sqlite3
import os

def check_database():
    db_path = 'atarys_data.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données {db_path} non trouvée")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Lister toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"📊 Base de données : {db_path}")
        print(f"📋 Tables trouvées ({len(tables)}):")
        
        for table in tables:
            table_name = table[0]
            print(f"\n📄 Table: {table_name}")
            
            # Structure de la table
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print("   Colonnes:")
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                print(f"   - {col_name} ({col_type})")
            
            # Nombre d'enregistrements
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   📊 {count} enregistrements")
            
            # Aperçu des données (5 premières lignes)
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                rows = cursor.fetchall()
                print("   Aperçu:")
                for i, row in enumerate(rows, 1):
                    print(f"   {i}. {row}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    check_database() 