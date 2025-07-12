#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - EXEMPLE DE MODÈLE AMÉLIORÉ
Exemple de modèle SQLAlchemy avec les bonnes pratiques pour les dates et valeurs par défaut

Auteur: ATARYS Team
Date: 2025
"""

from .base import BaseModel
from app import db
import datetime


class ExempleArticle(BaseModel):
    __tablename__ = 'exemple_articles'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # ✅ BONNES PRATIQUES - Colonnes avec valeurs par défaut intelligentes
    reference = db.Column(db.String(100), nullable=False, unique=True)
    libelle = db.Column(db.Text, nullable=False)
    
    # ✅ Montants financiers avec Numeric(10, 2) et valeurs par défaut
    prix_achat = db.Column(db.Numeric(10, 2), default=0.00)
    prix_unitaire = db.Column(db.Numeric(10, 2), default=0.00)
    tva_pct = db.Column(db.Numeric(10, 2), default=20.00)
    coefficient = db.Column(db.Numeric(10, 2), default=1.00)
    
    # ✅ Statut actif par défaut
    actif = db.Column(db.Boolean, default=True)
    
    # ✅ Dates avec valeurs par défaut automatiques
    date_import = db.Column(db.Date, default=datetime.date.today)
    date_maj = db.Column(db.Date, default=datetime.date.today)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # ✅ Autres colonnes avec valeurs par défaut
    unite = db.Column(db.String(20), default="PIECE")
    famille = db.Column(db.String(30), default="GENERAL")
    quantite_stock = db.Column(db.Integer, default=0)
    description = db.Column(db.Text, default="")
    
    def __repr__(self):
        return f'<ExempleArticle {self.id}>'


class ExempleChantier(BaseModel):
    __tablename__ = 'exemple_chantiers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # ✅ Informations de base
    nom = db.Column(db.String(200), nullable=False)
    adresse = db.Column(db.Text)
    
    # ✅ Statuts avec valeurs par défaut
    statut = db.Column(db.String(50), default="EN_COURS")
    actif = db.Column(db.Boolean, default=True)
    
    # ✅ Montants financiers
    montant_ht = db.Column(db.Numeric(10, 2), default=0.00)
    tva_pct = db.Column(db.Numeric(10, 2), default=20.00)
    
    # ✅ Dates avec valeurs par défaut
    date_creation = db.Column(db.Date, default=datetime.date.today)
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # ✅ Compteurs avec valeurs par défaut
    nombre_ouvriers = db.Column(db.Integer, default=0)
    duree_estimee = db.Column(db.Integer, default=0)  # en jours
    
    # ✅ Textes avec valeurs par défaut
    notes = db.Column(db.Text, default="")
    description = db.Column(db.Text, default="")
    
    def __repr__(self):
        return f'<ExempleChantier {self.id}>'


"""
✅ RÈGLES ATARYS RESPECTÉES :

1. DATES :
   - ✅ date_import = db.Column(db.Date, default=datetime.date.today)
   - ✅ date_maj = db.Column(db.Date, default=datetime.date.today)
   - ✅ created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
   - ✅ updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

2. STATUTS :
   - ✅ actif = db.Column(db.Boolean, default=True)

3. MONTANTS FINANCIERS :
   - ✅ prix_achat = db.Column(db.Numeric(10, 2), default=0.00)
   - ✅ tva_pct = db.Column(db.Numeric(10, 2), default=20.00)

4. COMPTEURS :
   - ✅ quantite_stock = db.Column(db.Integer, default=0)
   - ✅ nombre_ouvriers = db.Column(db.Integer, default=0)

5. TEXTES :
   - ✅ description = db.Column(db.Text, default="")
   - ✅ notes = db.Column(db.Text, default="")

6. IMPORTS :
   - ✅ import datetime (ajouté automatiquement par le générateur)

❌ PROBLÈMES ÉVITÉS :
- ❌ Pas de nullable=False sans valeur par défaut pour les dates
- ❌ Pas de valeurs par défaut manquantes pour les statuts
- ❌ Pas d'erreurs d'insertion à cause de contraintes non respectées
""" 