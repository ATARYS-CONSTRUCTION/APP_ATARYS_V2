import pandas as pd
import os
from app import create_app, db
from app.models.module_5_1 import articlesatarys

app = create_app('development')

def check_csv_consistency(csv_path):
    """Vérifie que toutes les lignes du CSV ont le même nombre de colonnes que l'en-tête."""
    with open(csv_path, encoding='utf-8') as f:
        lines = f.readlines()
    header_cols = len(lines[0].strip().split(';'))
    errors = []
    for i, line in enumerate(lines[1:], start=2):
        if len(line.strip().split(';')) != header_cols:
            errors.append((i, line.strip()))
    return header_cols, errors

def write_error_report(errors, csv_path):
    """Génère un rapport CSV des lignes fautives."""
    report_path = os.path.join(os.path.dirname(csv_path), 'erreurs_import.csv')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('ligne;contenu\n')
        for i, line in errors:
            f.write(f'{i};"{line}"\n')
    print(f"📝 Rapport d'erreur généré : {report_path}")

def import_articles_from_csv(csv_filename):
    # Chemin par défaut : data/import_csv/nom_du_fichier.csv (depuis la racine du projet)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'data', 'import_csv', csv_filename)
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Fichier CSV non trouvé : {csv_path}")
    # Vérification du CSV
    header_cols, errors = check_csv_consistency(csv_path)
    if errors:
        print(f"❌ Erreur : {len(errors)} ligne(s) du CSV n'ont pas {header_cols} colonnes :")
        for i, line in errors:
            print(f"  Ligne {i} : {line}")
        write_error_report(errors, csv_path)
        print("Corrige le fichier CSV avant de relancer l'import.")
        return
    df = pd.read_csv(csv_path, sep=';')
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