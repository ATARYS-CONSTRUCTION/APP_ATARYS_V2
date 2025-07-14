"""
Module 5 - Modèles SQLAlchemy
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

# Modèles du module 5 - DEVIS_FACTURATION

class TestModel(BaseModel):
    """Modèle de test pour vérifier Flask-Migrate"""
    __tablename__ = 'test_model'
    
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    montant = db.Column(db.Numeric(10, 2), default=0.00)
    actif = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<TestModel {self.nom}>'


from app.models.base import BaseModel
from app import db
from datetime import datetime
class TestProfessionalTable(BaseModel):
    __tablename__ = 'test_professional_table'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.String(100)(nullable=False)
    description = db.Text()
    montant = db.Numeric(10, 2)(nullable=False, default=0.0)
    actif = db.Boolean(nullable=False, default=true)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    def __repr__(self):
        return f'<TestProfessionalTable {self.id}>'
