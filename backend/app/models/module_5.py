"""
Module 5 - Modèles SQLAlchemy - DEVIS_FACTURATION
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Hérite toujours de BaseModel
- Utilise db.Numeric(10, 2) pour montants financiers
- Strings avec longueur max obligatoire
- __repr__ explicite
"""
from datetime import datetime
from app import db
from app.models.base import BaseModel


class FamilleOuvrages(BaseModel):
    __tablename__ = 'famille_ouvrages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_bd_atarys = db.Column(db.String(10))
    libelle = db.Column(db.String(100), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<FamilleOuvrages {self.id}>"
