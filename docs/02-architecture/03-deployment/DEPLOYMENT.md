# 🚀 Guide de Déploiement ATARYS

> **Guide complet pour le déploiement du système ATARYS**  
> Environnements : Développement, Staging, Production  
> Dernière mise à jour : 22/06/2025

---

## 🎯 **Vue d'Ensemble des Environnements**

### **Architecture de Déploiement**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  DÉVELOPPEMENT  │    │     STAGING     │    │   PRODUCTION    │
│                 │    │                 │    │                 │
│ Flask Dev       │    │ Flask + Gunicorn│    │ Flask + Gunicorn│
│ Vite Dev        │    │ Nginx + Build   │    │ Nginx + Build   │
│ SQLite Local    │    │ SQLite/PostgreSQL│   │ PostgreSQL      │
│ Port 5000/3001  │    │ Port 80/443     │    │ Port 80/443     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Stratégie de Déploiement**
- **Développement** : Hot reload, debug activé
- **Staging** : Production-like, tests automatisés
- **Production** : Optimisé, monitoring, backups

---

## 💻 **Environnement de Développement**

### **Prérequis**
```bash
# Python 3.11+
python --version

# Node.js 18+
node --version
npm --version

# Git
git --version
```

### **Installation Locale**

#### **1. Cloner le Projet**
```bash
git clone https://github.com/votre-org/atarys.git
cd atarys
```

#### **2. Configuration Backend**
```bash
# Créer l'environnement virtuel
cd backend
python -m venv venv

# Activer (Windows)
venv\Scripts\activate
# Activer (Linux/Mac)
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# ⚠️ IMPORTANT : Mise à jour Requirements
# Les requirements ont été récemment mis à jour avec pandas et openpyxl
# pour l'extraction de devis Excel (Module 3.1).
# Vérifier que requirements/base.txt contient :
# - pandas>=1.5.0 (traitement CSV/Excel)
# - openpyxl>=3.0.0 (lecture fichiers .xlsx)

# Configuration environnement
cp env.example .env
# Éditer .env selon vos besoins
```

#### **3. Configuration Frontend**
```bash
cd frontend
npm install

# Configuration environnement
cp .env.example .env.local
# Éditer .env.local selon vos besoins
```

#### **4. Base de Données**
```bash
# Vérifier que la base existe
ls -la data/atarys_data.db

# Si nécessaire, initialiser
cd backend
python init_db.py
```

### **Lancement Développement**

#### **Démarrage Backend**
```bash
cd backend
python run.py
# ✅ Serveur sur http://localhost:5000
```

#### **Démarrage Frontend**
```bash
cd frontend
npm run dev
# ✅ Interface sur http://localhost:3001
```

### **Variables d'Environnement Dev**

#### **Backend (`.env`)**
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_PATH=../data/atarys_data.db
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

#### **Frontend (`.env.local`)**
```env
VITE_API_URL=http://localhost:5000
VITE_ENV=development
```

---

## 🧪 **Environnement de Staging**

### **Infrastructure**

#### **Serveur de Staging**
```bash
# Spécifications recommandées
CPU: 2 vCPU
RAM: 4 GB
Stockage: 50 GB SSD
OS: Ubuntu 22.04 LTS
```

#### **Installation Serveur**
```bash
# Mise à jour système
sudo apt update && sudo apt upgrade -y

# Installation Python
sudo apt install python3.11 python3.11-venv python3-pip -y

# Installation Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Installation Nginx
sudo apt install nginx -y

# Installation PostgreSQL (optionnel)
sudo apt install postgresql postgresql-contrib -y
```

### **Déploiement Staging**

#### **1. Préparation du Code**
```bash
# Sur votre machine locale
git checkout staging
git pull origin staging

# Build frontend
cd frontend
npm run build

# Créer archive de déploiement
cd ..
tar -czf atarys-staging.tar.gz \
  --exclude=node_modules \
  --exclude=venv \
  --exclude=.git \
  .
```

#### **2. Déploiement sur Serveur**
```bash
# Copier sur serveur
scp atarys-staging.tar.gz user@staging-server:/opt/

# Sur le serveur
ssh user@staging-server
cd /opt
sudo tar -xzf atarys-staging.tar.gz
sudo chown -R www-data:www-data atarys/
```

#### **3. Configuration Backend Staging**
```bash
cd /opt/atarys/backend

# Environnement virtuel
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Variables d'environnement
sudo tee .env << EOF
FLASK_ENV=staging
FLASK_DEBUG=False
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_PATH=/opt/atarys/data/atarys_data.db
LOG_LEVEL=INFO
CORS_ORIGINS=https://staging.atarys.com
EOF
```

#### **4. Service Systemd**
```bash
# Créer service backend
sudo tee /etc/systemd/system/atarys-backend.service << EOF
[Unit]
Description=ATARYS Backend
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/atarys/backend
Environment=PATH=/opt/atarys/backend/venv/bin
ExecStart=/opt/atarys/backend/venv/bin/gunicorn --bind 127.0.0.1:5000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Activer et démarrer
sudo systemctl enable atarys-backend
sudo systemctl start atarys-backend
sudo systemctl status atarys-backend
```

#### **5. Configuration Nginx**
```bash
# Configuration Nginx
sudo tee /etc/nginx/sites-available/atarys-staging << EOF
server {
    listen 80;
    server_name staging.atarys.com;
    
    # Frontend statique
    location / {
        root /opt/atarys/frontend/dist;
        try_files \$uri \$uri/ /index.html;
    }
    
    # API Backend
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Assets statiques
    location /static/ {
        root /opt/atarys/backend;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Activer le site
sudo ln -s /etc/nginx/sites-available/atarys-staging /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### **SSL/HTTPS avec Let's Encrypt**
```bash
# Installation Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtenir certificat SSL
sudo certbot --nginx -d staging.atarys.com

# Renouvellement automatique
sudo crontab -e
# Ajouter : 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 🏭 **Environnement de Production**

### **Infrastructure Production**

#### **Spécifications Serveur**
```bash
# Serveur principal
CPU: 4+ vCPU
RAM: 8+ GB
Stockage: 100+ GB SSD
OS: Ubuntu 22.04 LTS

# Base de données (séparée)
CPU: 2+ vCPU
RAM: 4+ GB
Stockage: 50+ GB SSD + Backups
```

#### **Architecture Haute Disponibilité**
```
┌─────────────────┐    ┌─────────────────┐
│  Load Balancer  │    │     Backup      │
│    (Nginx)      │    │    Server       │
└─────────┬───────┘    └─────────────────┘
          │
    ┌─────┴─────┐
    │           │
┌───▼───┐   ┌───▼───┐
│App 1  │   │App 2  │
│Flask  │   │Flask  │
└───┬───┘   └───┬───┘
    │           │
    └─────┬─────┘
          │
    ┌─────▼─────┐
    │PostgreSQL │
    │ Cluster   │
    └───────────┘
```

### **Déploiement Production**

#### **1. Base de Données PostgreSQL**
```bash
# Installation PostgreSQL
sudo apt install postgresql-14 postgresql-contrib-14 -y

# Configuration
sudo -u postgres psql
postgres=# CREATE DATABASE atarys_prod;
postgres=# CREATE USER atarys_user WITH PASSWORD 'secure_password';
postgres=# GRANT ALL PRIVILEGES ON DATABASE atarys_prod TO atarys_user;
postgres=# \q

# Migration des données
pg_dump sqlite:///path/to/atarys_data.db | psql -h localhost -U atarys_user atarys_prod
```

#### **2. Configuration Application**
```bash
# Variables d'environnement production
sudo tee /opt/atarys/backend/.env << EOF
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=postgresql://atarys_user:secure_password@localhost/atarys_prod
LOG_LEVEL=WARNING
CORS_ORIGINS=https://atarys.com,https://www.atarys.com
SENTRY_DSN=https://your-sentry-dsn
EOF
```

#### **3. Service Production avec Gunicorn**
```bash
# Configuration Gunicorn
sudo tee /opt/atarys/backend/gunicorn.conf.py << EOF
bind = "127.0.0.1:5000"
workers = 4
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 5
user = "www-data"
group = "www-data"
tmp_upload_dir = None
EOF

# Service systemd production
sudo tee /etc/systemd/system/atarys-prod.service << EOF
[Unit]
Description=ATARYS Production
After=network.target postgresql.service

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/atarys/backend
Environment=PATH=/opt/atarys/backend/venv/bin
ExecStart=/opt/atarys/backend/venv/bin/gunicorn -c gunicorn.conf.py wsgi:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

#### **4. Configuration Nginx Production**
```bash
sudo tee /etc/nginx/sites-available/atarys-prod << EOF
# Rate limiting
limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;

# Upstream backend
upstream atarys_backend {
    server 127.0.0.1:5000;
    # Ajouter d'autres serveurs pour load balancing
    # server 127.0.0.1:5001;
}

server {
    listen 443 ssl http2;
    server_name atarys.com www.atarys.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/atarys.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/atarys.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    # Frontend
    location / {
        root /opt/atarys/frontend/dist;
        try_files \$uri \$uri/ /index.html;
        expires 1h;
    }
    
    # API avec rate limiting
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        
        proxy_pass http://atarys_backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
    }
    
    # Assets statiques avec cache long
    location /static/ {
        root /opt/atarys/backend;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}

# Redirection HTTP vers HTTPS
server {
    listen 80;
    server_name atarys.com www.atarys.com;
    return 301 https://\$server_name\$request_uri;
}
EOF
```

### **Monitoring et Logging**

#### **1. Configuration des Logs**
```bash
# Rotation des logs
sudo tee /etc/logrotate.d/atarys << EOF
/opt/atarys/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload atarys-prod
    endscript
}
EOF
```

#### **2. Monitoring avec Prometheus + Grafana**
```bash
# Installation Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.40.0/prometheus-2.40.0.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
sudo mv prometheus-2.40.0.linux-amd64 /opt/prometheus

# Configuration Prometheus
sudo tee /opt/prometheus/prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'atarys'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: '/metrics'
EOF
```

### **Sauvegarde et Récupération**

#### **Script de Sauvegarde**
```bash
#!/bin/bash
# /opt/scripts/backup-atarys.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/atarys"
DB_name="atarys_prod"

# Créer répertoire de sauvegarde
mkdir -p $BACKUP_DIR

# Sauvegarde base de données
pg_dump -h localhost -U atarys_user $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Sauvegarde fichiers application
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /opt/atarys/data/

# Sauvegarde logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz /opt/atarys/logs/

# Nettoyage (garder 30 jours)
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Sauvegarde terminée: $DATE"
```

#### **Cron de Sauvegarde**
```bash
# Sauvegarde quotidienne à 2h du matin
sudo crontab -e
0 2 * * * /opt/scripts/backup-atarys.sh >> /var/log/atarys-backup.log 2>&1
```

---

## 🔄 **CI/CD avec GitHub Actions**

### **Workflow de Déploiement**
```yaml
# .github/workflows/deploy.yml
name: Deploy ATARYS

on:
  push:
    branches: [main, staging]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install Backend Dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Install Frontend Dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Run Backend Tests
        run: |
          cd backend
          python -m pytest tests/ --cov=app
      
      - name: Run Frontend Tests
        run: |
          cd frontend
          npm test -- --coverage --watchAll=false
      
      - name: Build Frontend
        run: |
          cd frontend
          npm run build

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/staging'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Staging
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.STAGING_HOST }}
          username: ${{ secrets.STAGING_USER }}
          key: ${{ secrets.STAGING_SSH_KEY }}
          script: |
            cd /opt/atarys
            git pull origin staging
            cd frontend && npm ci && npm run build
            cd ../backend && source venv/bin/activate && pip install -r requirements.txt
            sudo systemctl restart atarys-backend
            sudo systemctl reload nginx

  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to Production
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /opt/atarys
            git pull origin main
            cd frontend && npm ci && npm run build
            cd ../backend && source venv/bin/activate && pip install -r requirements.txt
            sudo systemctl restart atarys-prod
            sudo systemctl reload nginx
```

---

## 🚀 **Migration vers Serveur Hébergé**

### **⚠️ Planification Migration Critique**

#### **Considérations Architecture**
La migration d'un environnement de développement local vers un serveur hébergé nécessite une planification spécifique pour ATARYS :

##### **🗄️ Base de Données**
```bash
# ACTUEL : SQLite local (développement)
DATABASE_PATH=../data/atarys_data.db

# FUTUR : PostgreSQL serveur hébergé
DATABASE_URL=postgresql://user:password@hostname:5432/atarys_prod
```

##### **📁 Stockage Fichiers**
- **Défi OneDrive** : Liens relatifs obligatoires (multi-appareils)
- **Solution** : Mapper OneDrive vers stockage cloud (AWS S3, etc.)
- **Migration** : Scripts de conversion chemins Windows → Linux

##### **🔧 Dépendances Critiques**
```bash
# Requirements spécifiques ATARYS
pandas>=1.5.0        # Extraction devis Excel (Module 3.1)
openpyxl>=3.0.0      # Lecture fichiers .xlsx
Flask-SQLAlchemy     # ORM base de données
```

#### **📋 Checklist Pré-Migration**

##### **Phase 1 : Préparation (2-3 semaines avant)**
- [ ] **Audit dépendances** : Vérifier compatibilité Linux des requirements
- [ ] **⚠️ CRITICAL - Mise à jour requirements** : S'assurer que TOUS les packages ajoutés pendant le développement sont dans requirements/base.txt
- [ ] **Test PostgreSQL** : Migration SQLite → PostgreSQL en local
- [ ] **OneDrive mapping** : Stratégie stockage cloud pour fichiers
- [ ] **Variables d'environnement** : Adaptation chemins absolus → relatifs
- [ ] **Performance** : Tests charge avec données production

##### **Phase 2 : Staging (1 semaine avant)**
- [ ] **Serveur staging** : Réplique exacte environnement production
- [ ] **Migration données** : Script SQLite → PostgreSQL validé
- [ ] **Tests fonctionnels** : Module 3.1 (extraction devis) + toutes APIs
- [ ] **Monitoring** : Logs, métriques, alertes configurées
- [ ] **Rollback plan** : Procédure retour arrière testée

##### **Phase 3 : Production (jour J)**
- [ ] **Sauvegarde complète** : SQLite + OneDrive + configuration
- [ ] **Coupure coordonnée** : Communication équipe ATARYS
- [ ] **Migration express** : Scripts automatisés < 2h downtime
- [ ] **Tests critiques** : Extraction devis, planning, chantiers
- [ ] **Go/No-Go** : Validation Julien + Yann avant ouverture

#### **🎯 Recommandations Hébergement ATARYS**

##### **Spécifications Serveur Minimum**
```
CPU: 4 vCPU (calculs pandas/Excel)
RAM: 8 GB (traitement fichiers volumineux)
SSD: 100 GB (base données + logs)
Bande passante: 1 Gbps (uploads devis Excel)
```

##### **Fournisseurs Recommandés**
- **OVH Cloud** : Français, RGPD natif, support FR
- **Scaleway** : Performance, proximité géographique
- **AWS Europe** : Robustesse, scaling automatique
- **DigitalOcean** : Simplicité, rapport qualité/prix

##### **Architecture Cible**
```
┌─────────────────────────────────────────────────┐
│                 LOAD BALANCER                   │
│                  (Nginx/HAProxy)                │
└─────────────────────┬───────────────────────────┘
                      │
         ┌────────────┴───────────┐
         │                        │
    ┌────▼────┐              ┌────▼────┐
    │  WEB 1  │              │  WEB 2  │
    │ Flask   │              │ Flask   │
    │ Gunicorn│              │ Gunicorn│
    └────┬────┘              └────┬────┘
         │                        │
         └────────────┬───────────┘
                      │
              ┌───────▼───────┐
              │   PostgreSQL  │
              │   + Backups   │
              └───────────────┘
```

#### **💡 Points d'Attention Spécifiques**
- **Module 3.1** : Extraction devis est critique → tests prioritaires
- **Performance** : pandas + Excel = consommation RAM importante
- **Sécurité** : Données entreprise sensibles (chantiers, devis, salariés)
- **Availability** : Équipe ATARYS travaille 8h-18h → maintenance possible soir/weekend

---

## 🔒 **Sécurité**

### **Checklist Sécurité**
- [ ] ✅ HTTPS activé avec certificats valides
- [ ] ✅ Rate limiting configuré
- [ ] ✅ Headers de sécurité ajoutés
- [ ] ✅ Firewall configuré (UFW)
- [ ] ✅ Mise à jour système automatiques
- [ ] ✅ Monitoring des intrusions
- [ ] ✅ Sauvegarde chiffrée
- [ ] ✅ Accès SSH par clés uniquement

### **Configuration Firewall**
```bash
# Configuration UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

---

## 📊 **Monitoring et Alertes**

### **Métriques à Surveiller**
- **Performance** : Temps de réponse API, CPU, RAM
- **Disponibilité** : Uptime, erreurs HTTP
- **Base de données** : Connexions, requêtes lentes
- **Sécurité** : Tentatives d'intrusion, erreurs 401/403

### **Alertes Critiques**
- CPU > 80% pendant 5 minutes
- RAM > 90% pendant 5 minutes
- Disque > 85% utilisé
- Erreurs 5xx > 1% des requêtes
- Base de données inaccessible

---

## 📋 **Checklist de Déploiement**

### **Avant Déploiement**
- [ ] ✅ Tests passent (unitaires + intégration)
- [ ] ✅ Build frontend réussi
- [ ] ✅ Variables d'environnement configurées
- [ ] ✅ Base de données migrée
- [ ] ✅ Sauvegarde effectuée

### **Après Déploiement**
- [ ] ✅ Application accessible
- [ ] ✅ APIs fonctionnelles
- [ ] ✅ Logs sans erreurs
- [ ] ✅ Monitoring actif
- [ ] ✅ Tests de fumée passés

### **En Cas de Problème**
1. **Vérifier les logs** : `/opt/atarys/logs/`
2. **Status services** : `systemctl status atarys-prod`
3. **Rollback** : `git checkout previous-commit && redeploy`
4. **Restauration DB** : Depuis sauvegarde la plus récente 