#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modèle SQLAlchemy pour la table articles_atarys
Généré automatiquement le 2025-07-12 20:16:42
"""

from app import db
from app.models.base import BaseModel

class ArticlesAtarys(BaseModel):
    __tablename__ = 'articles_atarys'
    
    reference = db.Column(db.String(100), nullable=False)
    libelle = db.Column(db.Text, nullable=False)
    prix_achat = db.Column(db.Numeric(10, 2))
    coefficient = db.Column(db.Numeric(10, 2))
    prix_unitaire = db.Column(db.Numeric(10, 2), nullable=False)
    unite = db.Column(db.String(20), nullable=False)
    tva_pct = db.Column(db.Numeric(10, 2), nullable=False)
    famille = db.Column(db.String(30))
    actif = db.Column(db.Boolean)
    date_import = db.Column(db.Date, nullable=False)
    date_maj = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<ArticlesAtarys {self.id}>'
