\# Documentation Architecture Batappli - Module Devis et Facturation



\## Vue d'ensemble de l'application existante



\### Architecture générale

L'application Batappli est une solution de gestion de matériaux et fournisseurs pour le bâtiment, organisée selon une architecture modulaire avec les composants suivants :





\## Analyse des composants existants



\### 1. Structure des données



\#### Base de données binaire (.bin)

\- \*\*Localisation\*\* : `Installation/`

\- \*\*Format\*\* : Fichiers binaires optimisés pour les performances

\- \*\*Contenu\*\* : Données de référence, configurations, paramètres

\- \*\*Avantage\*\* : Accès rapide, pas de requêtes SQL

\- \*\*Inconvénient\*\* : Pas de relations complexes, structure rigide



\#### Base de connaissances (.FIC, .ndx, .ftx)

\- \*\*Localisation\*\* : `Kb/`

\- \*\*Format\*\* : Fichiers indexés avec moteur de recherche

\- \*\*Contenu\*\* : Documentation, articles, références techniques

\- \*\*Structure\*\* :

&nbsp; - `.FIC` : Fichiers de données

&nbsp; - `.ndx` : Index de recherche

&nbsp; - `.ftx` : Fichiers texte

&nbsp; - `.mmo` : Métadonnées



\#### Formats fournisseurs (.fmt, .fmt2)

\- \*\*Localisation\*\* : `Fournisseurs/`

\- \*\*Format\*\* : Formats de données standardisés par fournisseur

\- \*\*Contenu\*\* : Catalogues, prix, références produits

\- \*\*Versions\*\* : `.fmt` (ancien), `.fmt2` (nouveau format)



\### 2. Modules et bibliothèques



\#### Bibliothèques principales (wd280\*.dll)

\- \*\*wd280sql.dll\*\* : Gestion des bases de données SQL

\- \*\*wd280sqlite.dll\*\* : Support SQLite

\- \*\*wd280xls.dll\*\* : Import/export Excel

\- \*\*wd280pdf.dll\*\* : Génération PDF

\- \*\*wd280html.dll\*\* : Interface web

\- \*\*wd280grf.dll\*\* : Graphiques et visualisations

\- \*\*wd280obj.dll\*\* : Objets métier

\- \*\*wd280vm.dll\*\* : Machine virtuelle pour scripts



\#### Modules métier

\- \*\*batiprixEngine.dll\*\* : Moteur de calcul des prix

\- \*\*xlsEngine.dll\*\* : Traitement Excel

\- \*\*printEngine.dll\*\* : Impression

\- \*\*adpEngine.dll\*\* : Adaptateurs de données



\### 3. Fonctionnalités identifiées



\#### Gestion des devis

\- Conversion de devis (`convertir\_devis.svg`)

\- Ouverture de devis (`ouvrirdevis.svg`)

\- Situations de devis (`situationsdevis`)

\- État en devis (`enDevis.svg`)



\#### Gestion des factures

\- Génération de factures (`enFacture.svg`)

\- Impression de factures (`imprimerfacture.svg`)

\- Gestion des factures (`mes\_factures.svg`, `factures.svg`)



\## Recommandations pour le nouveau module SQLAlchemy



\### 1. Architecture recommandée

Module\_Devis\_Facturation/

├── models/ # Modèles SQLAlchemy

│ ├── init.py

│ ├── devis.py # Modèle Devis

│ ├── facture.py # Modèle Facture

│ ├── client.py # Modèle Client

│ ├── produit.py # Modèle Produit

│ └── fournisseur.py # Modèle Fournisseur

├── services/ # Couche métier

│ ├── init.py

│ ├── devis\_service.py

│ ├── facture\_service.py

│ └── calcul\_service.py

├── controllers/ # Contrôleurs

│ ├── init.py

│ ├── devis\_controller.py

│ └── facture\_controller.py

├── views/ # Interface utilisateur

│ ├── init.py

│ ├── devis\_views.py

│ └── facture\_views.py

├── utils/ # Utilitaires

│ ├── init.py

│ ├── pdf\_generator.py

│ ├── excel\_exporter.py

│ └── validators.py

├── config/ # Configuration

│ ├── init.py

│ ├── database.py

│ └── settings.py

└── tests/ # Tests unitaires

├── init.py

├── test\_models.py

└── test\_services.py







\### 2. Modèles de données SQLAlchemy



\#### Modèle Devis

```python

class Devis(Base):

&nbsp;   \_\_tablename\_\_ = 'devis'

&nbsp;   

&nbsp;   id = Column(Integer, primary\_key=True)

&nbsp;   numero = Column(String(50), unique=True, nullable=False)

&nbsp;   date\_creation = Column(DateTime, default=datetime.utcnow)

&nbsp;   date\_validite = Column(DateTime)

&nbsp;   client\_id = Column(Integer, ForeignKey('clients.id'))

&nbsp;   statut = Column(Enum('brouillon', 'envoye', 'accepte', 'refuse'))

&nbsp;   montant\_ht = Column(Decimal(10, 2))

&nbsp;   montant\_ttc = Column(Decimal(10, 2))

&nbsp;   tva = Column(Decimal(5, 2), default=20.0)

&nbsp;   

&nbsp;   # Relations

&nbsp;   client = relationship("Client", back\_populates="devis")

&nbsp;   lignes = relationship("LigneDevis", back\_populates="devis")

```



\#### Modèle Facture

```python

class Facture(Base):

&nbsp;   \_\_tablename\_\_ = 'factures'

&nbsp;   

&nbsp;   id = Column(Integer, primary\_key=True)

&nbsp;   numero = Column(String(50), unique=True, nullable=False)

&nbsp;   date\_emission = Column(DateTime, default=datetime.utcnow)

&nbsp;   date\_echeance = Column(DateTime)

&nbsp;   devis\_id = Column(Integer, ForeignKey('devis.id'))

&nbsp;   client\_id = Column(Integer, ForeignKey('clients.id'))

&nbsp;   statut = Column(Enum('emise', 'payee', 'en\_retard'))

&nbsp;   montant\_ht = Column(Decimal(10, 2))

&nbsp;   montant\_ttc = Column(Decimal(10, 2))

&nbsp;   tva = Column(Decimal(5, 2), default=20.0)

&nbsp;   

&nbsp;   # Relations

&nbsp;   devis = relationship("Devis", back\_populates="factures")

&nbsp;   client = relationship("Client", back\_populates="factures")

&nbsp;   lignes = relationship("LigneFacture", back\_populates="facture")

```



\### 3. Services métier



\#### Service Devis

```python

class DevisService:

&nbsp;   def \_\_init\_\_(self, session):

&nbsp;       self.session = session

&nbsp;   

&nbsp;   def creer\_devis(self, client\_id, produits):

&nbsp;       """Créer un nouveau devis"""

&nbsp;       pass

&nbsp;   

&nbsp;   def calculer\_montants(self, devis\_id):

&nbsp;       """Calculer les montants HT et TTC"""

&nbsp;       pass

&nbsp;   

&nbsp;   def generer\_pdf(self, devis\_id):

&nbsp;       """Générer le PDF du devis"""

&nbsp;       pass

&nbsp;   

&nbsp;   def envoyer\_devis(self, devis\_id):

&nbsp;       """Envoyer le devis par email"""

&nbsp;       pass

```



\#### Service Facture

```python

class FactureService:

&nbsp;   def \_\_init\_\_(self, session):

&nbsp;       self.session = session

&nbsp;   

&nbsp;   def creer\_facture\_from\_devis(self, devis\_id):

&nbsp;       """Créer une facture à partir d'un devis accepté"""

&nbsp;       pass

&nbsp;   

&nbsp;   def generer\_facture\_pdf(self, facture\_id):

&nbsp;       """Générer le PDF de la facture"""

&nbsp;       pass

&nbsp;   

&nbsp;   def calculer\_echeances(self, facture\_id):

&nbsp;       """Calculer les échéances de paiement"""

&nbsp;       pass

```



\### 4. Intégration avec l'existant



\#### Adaptation des formats fournisseurs

```python

class FournisseurAdapter:

&nbsp;   """Adaptateur pour convertir les formats .fmt vers SQLAlchemy"""

&nbsp;   

&nbsp;   def importer\_catalogue(self, fichier\_fmt):

&nbsp;       """Importer un catalogue fournisseur"""

&nbsp;       pass

&nbsp;   

&nbsp;   def synchroniser\_prix(self, fournisseur\_id):

&nbsp;       """Synchroniser les prix avec le fournisseur"""

&nbsp;       pass

```



\#### Interface avec l'application principale

```python

class BatappliIntegration:

&nbsp;   """Interface avec l'application Batappli existante"""

&nbsp;   

&nbsp;   def importer\_clients(self):

&nbsp;       """Importer les clients depuis Batappli"""

&nbsp;       pass

&nbsp;   

&nbsp;   def exporter\_devis(self, devis\_id):

&nbsp;       """Exporter vers le format Batappli"""

&nbsp;       pass

```



\### 5. Configuration et déploiement



\#### Configuration de base de données

```python

\# config/database.py

from sqlalchemy import create\_engine

from sqlalchemy.orm import sessionmaker



DATABASE\_URL = "sqlite:///devis\_facturation.db"

engine = create\_engine(DATABASE\_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

```



\#### Migration des données existantes

```python

class DataMigration:

&nbsp;   """Migration des données depuis l'ancien format"""

&nbsp;   

&nbsp;   def migrer\_clients(self):

&nbsp;       """Migrer les clients depuis les fichiers .bin"""

&nbsp;       pass

&nbsp;   

&nbsp;   def migrer\_produits(self):

&nbsp;       """Migrer les produits depuis les formats .fmt"""

&nbsp;       pass

```



\### 6. Avantages de cette approche



\#### Par rapport à l'existant

\- \*\*Relations complexes\*\* : Support des relations entre entités

\- \*\*Requêtes avancées\*\* : Utilisation de SQL pour des requêtes complexes

\- \*\*Intégrité des données\*\* : Contraintes et validations automatiques

\- \*\*Évolutivité\*\* : Structure modulaire et extensible

\- \*\*Tests\*\* : Possibilité de tests unitaires et d'intégration



\#### Compatibilité

\- \*\*Import/Export\*\* : Conservation des formats d'échange existants

\- \*\*Interface\*\* : Réutilisation des composants d'interface

\- \*\*Données\*\* : Migration progressive des données existantes



\### 7. Plan de développement recommandé



\#### Phase 1 : Structure de base

1\. Créer les modèles SQLAlchemy

2\. Mettre en place la configuration de base de données

3\. Créer les services de base



\#### Phase 2 : Fonctionnalités métier

1\. Implémenter la gestion des devis

2\. Implémenter la gestion des factures

3\. Créer les générateurs PDF



\#### Phase 3 : Intégration

1\. Adapter les formats fournisseurs existants

2\. Créer les interfaces d'import/export

3\. Tester l'intégration avec l'application principale



\#### Phase 4 : Optimisation

1\. Optimiser les performances

2\. Ajouter des fonctionnalités avancées

3\. Finaliser la documentation



\### 8. Considérations techniques



\#### Performance

\- \*\*Indexation\*\* : Index sur les champs de recherche fréquents

\- \*\*Pagination\*\* : Gestion des grandes listes

\- \*\*Cache\*\* : Mise en cache des données fréquemment utilisées



\#### Sécurité

\- \*\*Validation\*\* : Validation des données d'entrée

\- \*\*Authentification\*\* : Gestion des droits d'accès

\- \*\*Audit\*\* : Traçabilité des modifications



\#### Maintenance

\- \*\*Logs\*\* : Journalisation des opérations

\- \*\*Backup\*\* : Sauvegarde automatique

\- \*\*Monitoring\*\* : Surveillance des performances



Cette architecture vous permettra de créer un module moderne et robuste tout en conservant la compatibilité avec votre application existante.

