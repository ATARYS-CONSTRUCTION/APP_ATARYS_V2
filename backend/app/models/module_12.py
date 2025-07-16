"""
Module 12 - Modèles SQLAlchemy - PARAMÈTRES
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Hérite toujours de BaseModel
- Utilise db.Numeric(10, 2) pour montants financiers
- Strings avec longueur max obligatoire
- __repr__ explicite
"""
from app.models.base import BaseModel
from app import db
from datetime import datetime

# Modèles du module 12 - PARAMÈTRES
# Ajouter ici les modèles du module 12 selon les besoins 


class TestAuditTable(BaseModel):
    __tablename__ = 'test_audit_table'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Numeric(10, 2))
    actif = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<TestAuditTable {self.id}>'
