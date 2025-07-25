"""
Module 10 - Modèles SQLAlchemy - OUTILS
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

# Modèles du module 10 - OUTILS
# Ajouter ici les modèles du module 10 selon les besoins


from app.models.base import BaseModel
from app import db
from datetime import datetime
class ModeleArdoises(BaseModel):
    __tablename__ = 'modele_ardoises'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    modele_ardoises = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    def __repr__(self):
        return f'<ModeleArdoises {self.id}>'



from app.models.base import BaseModel
from app import db
from datetime import datetime
class Villes(BaseModel):
    __tablename__ = 'villes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    communes = db.Column(db.String(100))
    code_postal = db.Column(db.Integer)
    code_insee = db.Column(db.Integer)
    departement = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    zone_nv = db.Column(db.Integer)
    distance_km_oiseau = db.Column(db.Float)
    distance_km_routes = db.Column(db.Float)
    temps_route_min = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    def __repr__(self):
        return f'<Villes {self.id}>'
