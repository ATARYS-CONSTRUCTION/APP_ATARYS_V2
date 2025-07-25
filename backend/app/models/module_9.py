"""
Module 9 - Modèles SQLAlchemy - SOCIAL
Respecte les standards ATARYS V2 (voir .cursorrules et 
docs/02-architecture/ATARYS_MODULES.md)
- Hérite toujours de BaseModel
- Utilise db.Numeric(10, 2) pour montants financiers
- Strings avec longueur max obligatoire
- __repr__ explicite
"""
from app.models.base import BaseModel
from app import db


class Ville(BaseModel):
    __tablename__ = 'villes'
    __table_args__ = {'extend_existing': True}
    
    # Informations de base
    communes = db.Column(db.String(100), nullable=False)
    code_postal = db.Column(db.Integer, nullable=False)
    code_insee = db.Column(db.Integer)
    departement = db.Column(db.Integer)
    
    # Coordonnées géographiques (gestion des virgules françaises)
    latitude = db.Column(db.String(20))  # Changé en String pour éviter les erreurs de conversion
    longitude = db.Column(db.String(20))  # Changé en String pour éviter les erreurs de conversion
    
    # Zone climatique
    zone_nv = db.Column(db.Integer)
    
    # Distances et temps (gestion des virgules françaises)
    distance_km_oiseau = db.Column(db.String(20))  # Changé en String
    distance_km_routes = db.Column(db.String(20))   # Changé en String
    temps_route_min = db.Column(db.String(20))      # Changé en String
    
    def __repr__(self):
        return f'<Ville {self.communes} ({self.code_postal})>'


class NiveauQualification(BaseModel):
    __tablename__ = 'niveau_qualification'
    
    # Informations de base
    niveau = db.Column(db.String(100), nullable=False)
    categorie = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<NiveauQualification {self.niveau}>'


# Table de liaison pour la relation many-to-many salaries <-> famille_ouvrages
salaries_famille_ouvrages = db.Table(
    'salaries_famille_ouvrages',
    db.Column('salaries_id', db.Integer, 
              db.ForeignKey('salaries.id'), primary_key=True),
    db.Column('famille_ouvrages_id', db.Integer, 
              db.ForeignKey('famille_ouvrages.id'), primary_key=True)
)


class Salaries(BaseModel):
    __tablename__ = 'salaries'
    
    # Informations de base (selon l'image)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    
    # Rémunération et heures (selon l'image)
    salaire_brut_horaire = db.Column(db.Numeric(10, 2), default=0.00)
    nbre_heure_hebdo = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Contrat
    type_contrat = db.Column(db.String(50), default='CDI')
    date_entree = db.Column(db.Date, nullable=False)
    date_sortie = db.Column(db.Date)
    
    # Qualifications
    niveau_qualification_id = db.Column(
        db.Integer, db.ForeignKey('niveau_qualification.id'))
    
    # Planning
    colonne_planning = db.Column(db.String(100))
    
    # Contact
    email = db.Column(db.String(200))
    num_telephone = db.Column(db.String(20))
    
    # Adresse
    adresse = db.Column(db.String(200))
    ville_id = db.Column(db.Integer, db.ForeignKey('villes.id'))
    
    # Informations personnelles
    date_naissance = db.Column(db.Date)
    num_securite_social = db.Column(db.String(20))
    
    # OneDrive
    ondrive_path = db.Column(db.String(500))
    
    # Relations
    niveau_qualification = db.relationship('NiveauQualification',
                                         backref='salaries')
    ville = db.relationship('Ville', backref='salaries')
    famille_ouvrages = db.relationship(
        'FamilleOuvrages',
        secondary=salaries_famille_ouvrages,
        backref=db.backref('salaries', lazy='dynamic')
    )
    
    def __repr__(self):
        return f'<Salaries {self.nom} {self.prenom}>'
