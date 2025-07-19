"""
Module 12 - Modèles SQLAlchemy - PARAMÈTRES
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
from app.models.module_9 import NiveauQualification


class TestAuditTable(BaseModel):
    __tablename__ = 'test_audit_table'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100))
    prix = db.Column(db.Float)
    actif = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TestAuditTable {self.id}>'


class TestCle2(BaseModel):
    __tablename__ = 'test_cle2'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(30))
    
    # Clé étrangère avec contrainte
    niveau_qualification_id = db.Column(
        db.Integer,
        db.ForeignKey('niveau_qualification.id', ondelete='SET NULL'),
        nullable=True
    )
    
    # Relation avec NiveauQualification
    niveau_qualification = db.relationship(
        'NiveauQualification',
        backref=db.backref('test_cles', lazy=True)
    )
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    def __repr__(self):
        return f'<TestCle2 {self.id}>'
