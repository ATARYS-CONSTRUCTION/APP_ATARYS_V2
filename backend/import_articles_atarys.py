import pandas as pd
import os
from app import create_app, db
from app.models.module_5_1 import articlesatarys

app = create_app('development')

def import_articles_from_csv(csv_filename):
    # Chemin par défaut : data/import_csv/nom_du_fichier.csv (depuis la racine du projet)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'data', 'import_csv', csv_filename)
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Fichier CSV non trouvé : {csv_path}")
    df = pd.read_csv(csv_path)
    with app.app_context():
        for _, row in df.iterrows():
            article = articlesatarys(
                reference=row['reference'],
                libelle=row['libelle'],
                prix_achat=row['prix_achat'],
                coefficient=row['coefficient'],
                prix_unitaire=row['prix_unitaire'],
                unite=row['unite'],
                tva_pct=row['tva_pct'],
                famille=row['famille'],
                actif=row['actif'],
                date_import=row['date_import'],
                date_maj=row['date_maj']
            )
            db.session.add(article)
        db.session.commit()
        print(f"{len(df)} articles importés avec succès.")

if __name__ == '__main__':
    # Demander le nom du fichier à l'utilisateur
    filename = input("Nom du fichier CSV à importer (ex: mon_fichier_articles.csv) : ")
    import_articles_from_csv(filename) 