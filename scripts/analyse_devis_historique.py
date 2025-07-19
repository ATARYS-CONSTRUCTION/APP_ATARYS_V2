#!/usr/bin/env python3
"""
Analyse des devis historiques ATARYS avec IA
Usage immédiat - avant même que le logiciel soit terminé
"""

import os
import json
import pandas as pd
from pathlib import Path
import PyPDF2
from openai import OpenAI
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re

class AnalyseurDevisATARYS:
    def __init__(self, api_key_openai):
        self.client = OpenAI(api_key=api_key_openai)
        self.devis_data = []
        
    def extraire_texte_pdf(self, chemin_pdf):
        """Extrait le texte d'un PDF"""
        try:
            with open(chemin_pdf, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                texte = ""
                for page in reader.pages:
                    texte += page.extract_text()
                return texte
        except Exception as e:
            print(f"Erreur lecture PDF {chemin_pdf}: {e}")
            return ""
    
    def analyser_devis_ia(self, texte_devis, nom_fichier):
        """Analyse un devis avec GPT-4"""
        prompt = f"""
        Analyse ce devis de construction et extrait les informations suivantes au format JSON :
        
        {{
            "fichier": "{nom_fichier}",
            "client_nom": "nom du client",
            "date_devis": "YYYY-MM-DD ou null",
            "montant_ht": 0.0,
            "montant_ttc": 0.0,
            "type_travaux": "toiture/façade/isolation/etc",
            "surface_m2": 0.0,
            "materiau_principal": "ardoise/zinc/tuile/etc",
            "delai_jours": 0,
            "main_oeuvre_ht": 0.0,
            "materiaux_ht": 0.0,
            "ville": "ville du chantier",
            "statut": "accepté/refusé/en_attente",
            "notes": "observations particulières"
        }}
        
        Texte du devis :
        {texte_devis[:3000]}...
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es un expert comptable BTP spécialisé dans l'analyse de devis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            # Parse la réponse JSON
            resultat = json.loads(response.choices[0].message.content)
            return resultat
            
        except Exception as e:
            print(f"Erreur analyse IA: {e}")
            return None
    
    def scanner_dossier_devis(self, chemin_dossier):
        """Scanne un dossier de devis PDF"""
        chemin = Path(chemin_dossier)
        fichiers_pdf = list(chemin.rglob("*.pdf"))
        
        print(f"🔍 Trouvé {len(fichiers_pdf)} fichiers PDF")
        
        for i, fichier_pdf in enumerate(fichiers_pdf, 1):
            print(f"📄 Analyse {i}/{len(fichiers_pdf)}: {fichier_pdf.name}")
            
            # Extraction texte
            texte = self.extraire_texte_pdf(fichier_pdf)
            if not texte:
                continue
                
            # Analyse IA
            analyse = self.analyser_devis_ia(texte, fichier_pdf.name)
            if analyse:
                analyse['chemin_fichier'] = str(fichier_pdf)
                self.devis_data.append(analyse)
                
        print(f"✅ Analysé {len(self.devis_data)} devis avec succès")
    
    def generer_rapport_analyse(self):
        """Génère un rapport d'analyse complet"""
        if not self.devis_data:
            print("❌ Aucune donnée à analyser")
            return
            
        df = pd.DataFrame(self.devis_data)
        
        # Nettoyage des données
        df['montant_ht'] = pd.to_numeric(df['montant_ht'], errors='coerce')
        df['date_devis'] = pd.to_datetime(df['date_devis'], errors='coerce')
        df['surface_m2'] = pd.to_numeric(df['surface_m2'], errors='coerce')
        
        print("\n" + "="*50)
        print("📊 RAPPORT D'ANALYSE DES DEVIS ATARYS")
        print("="*50)
        
        # Statistiques générales
        print(f"\n📈 STATISTIQUES GÉNÉRALES:")
        print(f"   • Nombre total de devis: {len(df)}")
        print(f"   • Montant total HT: {df['montant_ht'].sum():,.2f} €")
        print(f"   • Montant moyen HT: {df['montant_ht'].mean():,.2f} €")
        print(f"   • Montant médian HT: {df['montant_ht'].median():,.2f} €")
        
        # Analyse par type de travaux
        print(f"\n🏗️ RÉPARTITION PAR TYPE DE TRAVAUX:")
        type_travaux = df['type_travaux'].value_counts()
        for travaux, count in type_travaux.items():
            pourcentage = (count / len(df)) * 100
            montant_moyen = df[df['type_travaux'] == travaux]['montant_ht'].mean()
            print(f"   • {travaux}: {count} devis ({pourcentage:.1f}%) - Moy: {montant_moyen:,.0f}€")
        
        # Analyse par matériau
        print(f"\n🧱 RÉPARTITION PAR MATÉRIAU:")
        materiaux = df['materiau_principal'].value_counts()
        for materiau, count in materiaux.head(5).items():
            pourcentage = (count / len(df)) * 100
            print(f"   • {materiau}: {count} devis ({pourcentage:.1f}%)")
        
        # Analyse temporelle
        if df['date_devis'].notna().any():
            print(f"\n📅 ÉVOLUTION TEMPORELLE:")
            df_dates = df.dropna(subset=['date_devis'])
            df_dates['annee'] = df_dates['date_devis'].dt.year
            evolution = df_dates.groupby('annee').agg({
                'montant_ht': ['count', 'sum', 'mean']
            }).round(2)
            print(evolution)
        
        # Taux de conversion (si statut disponible)
        if 'statut' in df.columns:
            print(f"\n💰 TAUX DE CONVERSION:")
            statuts = df['statut'].value_counts()
            for statut, count in statuts.items():
                pourcentage = (count / len(df)) * 100
                print(f"   • {statut}: {count} devis ({pourcentage:.1f}%)")
        
        # Sauvegarde des résultats
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fichier_excel = f"analyse_devis_atarys_{timestamp}.xlsx"
        df.to_excel(fichier_excel, index=False)
        print(f"\n💾 Données sauvegardées dans: {fichier_excel}")
        
        return df
    
    def generer_graphiques(self, df):
        """Génère des graphiques d'analyse"""
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Graphique 1: Distribution des montants
        axes[0,0].hist(df['montant_ht'].dropna(), bins=20, alpha=0.7, color='skyblue')
        axes[0,0].set_title('Distribution des Montants HT')
        axes[0,0].set_xlabel('Montant HT (€)')
        axes[0,0].set_ylabel('Nombre de devis')
        
        # Graphique 2: Top types de travaux
        type_travaux = df['type_travaux'].value_counts().head(8)
        axes[0,1].bar(range(len(type_travaux)), type_travaux.values, color='lightcoral')
        axes[0,1].set_title('Top Types de Travaux')
        axes[0,1].set_xticks(range(len(type_travaux)))
        axes[0,1].set_xticklabels(type_travaux.index, rotation=45)
        
        # Graphique 3: Évolution temporelle
        if df['date_devis'].notna().any():
            df_dates = df.dropna(subset=['date_devis'])
            df_dates['mois'] = df_dates['date_devis'].dt.to_period('M')
            evolution = df_dates.groupby('mois')['montant_ht'].sum()
            axes[1,0].plot(evolution.index.astype(str), evolution.values, marker='o')
            axes[1,0].set_title('Évolution du CA par Mois')
            axes[1,0].tick_params(axis='x', rotation=45)
        
        # Graphique 4: Prix au m²
        df_surface = df.dropna(subset=['surface_m2', 'montant_ht'])
        if len(df_surface) > 0:
            df_surface['prix_m2'] = df_surface['montant_ht'] / df_surface['surface_m2']
            axes[1,1].scatter(df_surface['surface_m2'], df_surface['prix_m2'], alpha=0.6)
            axes[1,1].set_title('Prix au m² vs Surface')
            axes[1,1].set_xlabel('Surface (m²)')
            axes[1,1].set_ylabel('Prix au m² (€)')
        
        plt.tight_layout()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(f'graphiques_analyse_devis_{timestamp}.png', dpi=300, bbox_inches='tight')
        print(f"📊 Graphiques sauvegardés: graphiques_analyse_devis_{timestamp}.png")
        plt.show()

def main():
    """Fonction principale"""
    print("🚀 ANALYSEUR DE DEVIS ATARYS - IA")
    print("=" * 40)
    
    # Configuration
    API_KEY = input("🔑 Clé API OpenAI: ").strip()
    if not API_KEY:
        print("❌ Clé API requise")
        return
    
    DOSSIER_DEVIS = input("📁 Chemin vers vos devis PDF (ex: C:\\ATARYS\\Devis): ").strip()
    if not os.path.exists(DOSSIER_DEVIS):
        print("❌ Dossier introuvable")
        return
    
    # Lancement de l'analyse
    analyseur = AnalyseurDevisATARYS(API_KEY)
    analyseur.scanner_dossier_devis(DOSSIER_DEVIS)
    
    if analyseur.devis_data:
        df = analyseur.generer_rapport_analyse()
        
        # Génération des graphiques
        reponse = input("\n📊 Générer les graphiques ? (o/n): ").lower()
        if reponse == 'o':
            analyseur.generer_graphiques(df)
    
    print("\n✅ Analyse terminée !")

if __name__ == "__main__":
    main()
