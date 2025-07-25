"""
Module 3 - Modèles SQLAlchemy - CHANTIERS
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


class Clients(BaseModel):
    """
    Table des clients ATARYS
    """
    __tablename__ = 'clients'
    
    # Informations de base
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(200))
    num_telephone = db.Column(db.String(20))
    
    # Adresse
    adresse = db.Column(db.String(200))
    code_postal = db.Column(db.String(10))  # String pour codes postaux
    
    # Relations avec autres tables
    ville_id = db.Column(
        db.Integer, 
        db.ForeignKey('villes.id', ondelete='SET NULL'), 
        nullable=True
    )
    
    # Informations professionnelles
    siret = db.Column(db.String(14))  # String pour SIRET
    id_contact_google = db.Column(db.String(100))
    
    # Relations Python
    ville = db.relationship('Ville', backref='clients', lazy='select')
    
    def __repr__(self):
        return f'<Clients {self.nom} {self.prenom}>'


# Les modèles Chantier et Client seront créés plus tard
# quand les tables correspondantes seront nécessaires
