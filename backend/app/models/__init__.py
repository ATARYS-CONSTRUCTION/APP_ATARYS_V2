# Import des modèles ATARYS V2
# Génération automatique - Ne pas modifier manuellement

# Ce fichier sera mis à jour automatiquement par auto_model_generator.py

# Dynamically import all module_*.py files so that SQLAlchemy metadata
# contains every generated model (obligatoire pour Alembic --autogenerate).
# This avoids having to manually update this file after each table creation.

import importlib
import pkgutil
from pathlib import Path

package_dir = Path(__file__).parent
for _, module_name, _ in pkgutil.iter_modules([str(package_dir)]):
    if module_name.startswith('module_'):
        importlib.import_module(f'app.models.{module_name}')
