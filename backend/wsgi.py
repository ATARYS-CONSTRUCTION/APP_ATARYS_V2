#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - FICHIER WSGI POUR DÉPLOIEMENT
Point d'entrée WSGI pour l'application Flask ATARYS

Auteur: ATARYS Team
Date: 2025
Version: 2.0
"""

from app import create_app

# Création de l'application Flask via Factory pattern
application = create_app()

if __name__ == '__main__':
    # Lancement du serveur de développement
    application.run(
        host='0.0.0.0',
        port=5000,
        debug=False
    ) 