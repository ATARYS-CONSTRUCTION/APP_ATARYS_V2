#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - APPLICATION FLASK V2
Factory pattern pour création de l'application Flask ATARYS

Auteur: ATARYS Team
Date: 2025
Version: 2.0 - Génération automatique
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


# Initialisation des extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='development'):
    """
    Factory pattern pour création de l'application Flask ATARYS
    
    Args:
        config_name (str): Nom de la configuration ('development', 'production', 'testing')
    
    Returns:
        Flask: Instance de l'application Flask configurée
    """
    
    # Créer l'instance Flask
    app = Flask(__name__)
    
    # Configuration de base
    # Base de données dans le dossier data/ à la racine du projet
    db_uri = 'sqlite:///../../data/atarys_data.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'atarys-secret-key-change-in-production'
    
    # Initialiser les extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Enregistrement des blueprints API

    # Enregistrement du blueprint générateur de tables
    try:
        from app.routes.table_generator import table_generator_bp
        app.register_blueprint(table_generator_bp)
        print("[ATARYS] Blueprint table_generator enregistré avec succès")
    except Exception as e:
        import traceback
        print(f"[ATARYS] Blueprint table_generator non chargé : {e}")
        print(f"[ATARYS] Traceback complet : {traceback.format_exc()}")

    # Enregistrement du blueprint table_sync
    try:
        from app.routes.table_sync import table_sync_bp
        app.register_blueprint(table_sync_bp)
        print("[ATARYS] Blueprint table_sync enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint table_sync non chargé : {e}")

    # Enregistrement du blueprint relation_generator
    try:
        from app.routes.relation_generator import relation_generator_bp
        app.register_blueprint(relation_generator_bp)
        print("[ATARYS] Blueprint relation_generator enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint relation_generator non chargé : {e}")

    # Enregistrement du blueprint database_api (nouveau service unifié)
    try:
        from app.routes.database_api import database_api_bp
        app.register_blueprint(database_api_bp)
        print("[ATARYS] Blueprint database_api enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint database_api non chargé : {e}")

    # Enregistrement des modules existants
    try:
        from app.routes.module_1 import module_1_bp
        app.register_blueprint(module_1_bp)
        print("[ATARYS] Blueprint module_1 enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint module_1 non chargé : {e}")

    try:
        from app.routes.module_2 import module_2_bp
        app.register_blueprint(module_2_bp)
        print("[ATARYS] Blueprint module_2 enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint module_2 non chargé : {e}")

    try:
        from app.routes.module_3 import module_3_bp
        app.register_blueprint(module_3_bp)
        print("[ATARYS] Blueprint module_3 enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint module_3 non chargé : {e}")

    try:
        from app.routes.module_4 import module_4_bp
        app.register_blueprint(module_4_bp)
        print("[ATARYS] Blueprint module_4 enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint module_4 non chargé : {e}")

    try:
        from app.routes.module_5 import module_5_bp
        app.register_blueprint(module_5_bp)
        print("[ATARYS] Blueprint module_5 enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint module_5 non chargé : {e}")

    # Enregistrement des modules 6 à 13
    try:
        from app.routes.module_6 import module_6_bp
        app.register_blueprint(module_6_bp)
        print("[ATARYS] Blueprint module_6 enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint module_6 non chargé : {e}")

    try:
        from app.routes.module_7 import module_7_bp
        app.register_blueprint(module_7_bp)
        print("[ATARYS] Blueprint module_7 enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint module_7 non chargé : {e}")

    try:
        from app.routes.module_8 import module_8_bp
        app.register_blueprint(module_8_bp)
        print("[ATARYS] Blueprint module_8 enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint module_8 non chargé : {e}")

    try:
        from app.routes.module_9 import module_9_bp
        app.register_blueprint(module_9_bp)
        print("[ATARYS] Blueprint module_9 enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint module_9 non chargé : {e}")

    try:
        from app.routes.module_10 import module_10_bp
        app.register_blueprint(module_10_bp)
        print("[ATARYS] Blueprint module_10 enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint module_10 non chargé : {e}")

    try:
        from app.routes.module_11 import module_11_bp
        app.register_blueprint(module_11_bp)
        print("[ATARYS] Blueprint module_11 enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint module_11 non chargé : {e}")

    try:
        from app.routes.module_12 import module_12_bp
        app.register_blueprint(module_12_bp)
        print("[ATARYS] Blueprint module_12 enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint module_12 non chargé : {e}")

    try:
        from app.routes.module_13 import module_13_bp
        app.register_blueprint(module_13_bp)
        print("[ATARYS] Blueprint module_13 enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint module_13 non chargé : {e}")

    # Enregistrement du blueprint Google Contacts
    try:
        from app.routes.google_contacts_api import google_contacts_bp
        app.register_blueprint(google_contacts_bp)
        print("[ATARYS] Blueprint google_contacts enregistré avec succès")
    except Exception as e:
        print(f"[ATARYS] Blueprint google_contacts non chargé : {e}")

    # Route de santé pour vérifier que l'app fonctionne
    @app.route('/health')
    def health_check():
        """Route de santé pour vérifier l'état de l'application"""
        return {
            'status': 'healthy',
            'environment': config_name,
            'database': 'connected' if db.engine else 'disconnected',
            'message': 'ATARYS Flask V2 app is running'
        }
    
    return app 