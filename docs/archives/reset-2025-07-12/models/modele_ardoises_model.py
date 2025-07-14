#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modèle SQLAlchemy pour la table modele_ardoises
Généré automatiquement le 2025-07-12 20:16:44
"""

from app import db
from app.models.base import BaseModel

class ModeleArdoises(BaseModel):
    __tablename__ = 'modele_ardoises'
    
    modele_ardoise = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<ModeleArdoises {self.id}>'
