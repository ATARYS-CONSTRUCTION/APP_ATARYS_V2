#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - APPLICATION FLASK
Factory pattern pour création de l'application Flask ATARYS

Auteur: ATARYS Team
Date: 2025
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
    try:
        from app.routes.articles_atarys import bp as articles_atarys_bp
        app.register_blueprint(articles_atarys_bp)
    except Exception as e:
        print(f"[ATARYS] Blueprint articles_atarys non chargé : {e}")
    
    try:
        from app.routes.create_table import bp as create_table_bp
        app.register_blueprint(create_table_bp)
    except Exception as e:
        print(f"[ATARYS] Blueprint create_table non chargé : {e}")
    
    # Route de santé pour vérifier que l'app fonctionne
    @app.route('/health')
    def health_check():
        """Route de santé pour vérifier l'état de l'application"""
        return {
            'status': 'healthy',
            'environment': config_name,
            'database': 'connected' if db.engine else 'disconnected',
            'message': 'ATARYS Flask app is running'
        }
    
    return app 