import os
import re

MODELS_DIR = os.path.join('backend', 'app', 'models')
ADMIN_FILE = os.path.join('backend', 'run_flask_admin.py')
DOC_FILE = os.path.join('docs', '02-architecture', 'API_ENDPOINTS.md')

# 1. Lister toutes les classes BaseModel dans models/
def list_model_classes():
    classes = set()
    for fname in os.listdir(MODELS_DIR):
        if fname.endswith('.py') and fname != '__init__.py':
            with open(os.path.join(MODELS_DIR, fname), encoding='utf-8') as f:
                for line in f:
                    m = re.match(r'class\s+(\w+)\(BaseModel\):', line)
                    if m:
                        classes.add(m.group(1))
    return classes

# 2. Lister les classes importées dans run_flask_admin.py
def list_admin_imports():
    imports = set()
    with open(ADMIN_FILE, encoding='utf-8') as f:
        for line in f:
            m = re.match(r'from app.models.\w+ import (\w+)', line)
            if m:
                imports.add(m.group(1))
    return imports

# 3. Générer le rapport
if __name__ == '__main__':
    model_classes = list_model_classes()
    admin_imports = list_admin_imports()
    orphelins = model_classes - admin_imports

    print("\n=== SYNCHRONISATION FLASK-ADMIN / MODELS ===\n")
    print(f"Modèles trouvés dans models/: {sorted(model_classes)}")
    print(f"Modèles importés dans run_flask_admin.py: {sorted(admin_imports)}")
    print()
    if orphelins:
        print("Modèles non importés dans l'admin (non visibles) :")
        for cls in sorted(orphelins):
            print(f" - {cls}")
    else:
        print("✅ Tous les modèles sont importés dans l'admin.")

    # 4. Générer un résumé Markdown pour la doc
    md = [
        "\n## Synchronisation Flask-Admin / Modèles (généré automatiquement)",
        f"- Modèles présents dans backend/app/models/: {', '.join(sorted(model_classes))}",
        f"- Modèles importés dans run_flask_admin.py : {', '.join(sorted(admin_imports))}",
    ]
    if orphelins:
        md.append(f"- ❗ Modèles non importés (non visibles dans l'admin) : {', '.join(sorted(orphelins))}")
    else:
        md.append("- ✅ Tous les modèles sont importés dans l'admin.")

    # Ajout automatique dans la doc API_ENDPOINTS.md
    try:
        with open(DOC_FILE, encoding='utf-8') as f:
            doc = f.read()
        # Remplace ou ajoute la section
        new_doc = re.sub(r'(## Synchronisation Flask-Admin / Modèles \(généré automatiquement\)[\s\S]*?)(\n## |\Z)', '\n'.join(md) + '\n\2', doc, flags=re.MULTILINE)
        with open(DOC_FILE, 'w', encoding='utf-8') as f:
            f.write(new_doc)
        print("\n✅ Documentation API_ENDPOINTS.md mise à jour.")
    except Exception as e:
        print(f"\n⚠️ Impossible de mettre à jour la doc automatiquement : {e}") 