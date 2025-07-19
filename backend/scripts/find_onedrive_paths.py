#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - TROUVER CHEMINS ONEDRIVE
Script pour trouver les chemins OneDrive sur le système

Auteur: ATARYS Team
Date: 2025
"""

import os
import glob
from pathlib import Path

def find_onedrive_paths():
    """Trouver les chemins OneDrive sur le système"""
    
    print("🔍 ATARYS - RECHERCHE CHEMINS ONEDRIVE")
    print("="*50)
    
    # Chemins possibles pour OneDrive
    possible_paths = [
        # Chemins utilisateur standard
        os.path.expanduser("~/OneDrive"),
        os.path.expanduser("~/OneDrive - Entreprise"),
        os.path.expanduser("~/OneDrive - Personnel"),
        
        # Chemins absolus courants
        "C:/Users/*/OneDrive",
        "C:/Users/*/OneDrive - Entreprise",
        "C:/Users/*/OneDrive - Personnel",
        "D:/OneDrive",
        "E:/OneDrive",
        
        # Chemins réseau possibles
        "//serveur/OneDrive",
        "//192.168.*/OneDrive"
    ]
    
    found_paths = []
    
    for path_pattern in possible_paths:
        try:
            # Si c'est un pattern avec wildcard
            if '*' in path_pattern:
                matches = glob.glob(path_pattern)
                for match in matches:
                    if os.path.exists(match):
                        found_paths.append(match)
            else:
                # Chemin direct
                if os.path.exists(path_pattern):
                    found_paths.append(path_pattern)
        except Exception as e:
            print(f"❌ Erreur avec {path_pattern}: {e}")
    
    if not found_paths:
        print("❌ Aucun dossier OneDrive trouvé")
        print("\n💡 Suggestions :")
        print("1. Vérifiez que OneDrive est installé")
        print("2. Cherchez manuellement dans l'explorateur de fichiers")
        print("3. Utilisez un chemin relatif depuis votre projet")
        return
    
    print(f"✅ {len(found_paths)} dossier(s) OneDrive trouvé(s) :")
    print("\n" + "="*50)
    
    for i, path in enumerate(found_paths, 1):
        print(f"\n📁 {i}. {path}")
        
        # Vérifier s'il y a des sous-dossiers intéressants
        try:
            subdirs = [d for d in os.listdir(path) 
                      if os.path.isdir(os.path.join(path, d))]
            
            if subdirs:
                print("   📂 Sous-dossiers disponibles :")
                for subdir in subdirs[:10]:  # Limiter à 10
                    print(f"      - {subdir}")
                if len(subdirs) > 10:
                    print(f"      ... et {len(subdirs) - 10} autres")
            else:
                print("   📂 Aucun sous-dossier")
                
        except Exception as e:
            print(f"   ❌ Erreur lecture: {e}")
    
    print("\n" + "="*50)
    print("🎯 RECOMMANDATIONS :")
    print("\n1. **Pour un seul poste** :")
    print("   Utilisez le chemin absolu complet")
    print("   Exemple: C:\\Users\\VotreNom\\OneDrive\\Administration")
    
    print("\n2. **Pour plusieurs postes** :")
    print("   Créez une structure identique sur tous les postes")
    print("   Utilisez des chemins relatifs")
    print("   Exemple: ./OneDrive/Administration")
    
    print("\n3. **Pour tester** :")
    print("   Créez un dossier de test dans votre projet")
    print("   Exemple: ./test_onedrive/Administration")

def create_test_structure():
    """Créer une structure de test pour OneDrive"""
    
    print("\n🔧 CRÉATION STRUCTURE DE TEST")
    print("="*40)
    
    # Créer un dossier de test dans le projet
    test_path = Path(__file__).parent.parent.parent / "test_onedrive"
    
    try:
        test_path.mkdir(exist_ok=True)
        
        # Créer la structure de test
        structure = [
            "Administration",
            "Administration/Volet social",
            "Administration/Volet social/0-Dc",
            "Documents",
            "Documents/Salariés"
        ]
        
        for folder in structure:
            folder_path = test_path / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Créé: {folder_path}")
        
        print(f"\n📁 Structure de test créée dans : {test_path}")
        print("💡 Vous pouvez maintenant utiliser :")
        print(f"   ./test_onedrive/Administration/Volet social/0-Dc")
        
    except Exception as e:
        print(f"❌ Erreur création structure: {e}")

if __name__ == "__main__":
    # Étape 1: Chercher les chemins OneDrive existants
    find_onedrive_paths()
    
    # Étape 2: Proposer de créer une structure de test
    response = input("\n🤔 Voulez-vous créer une structure de test ? (o/n): ").lower()
    if response in ['o', 'oui', 'y', 'yes']:
        create_test_structure()
    
    print("\n🎯 Instructions pour le frontend:")
    print("1. Ouvrir l'application sur http://localhost:3001")
    print("2. Aller dans Module 9.1 - Salariés")
    print("3. Éditer un salarié")
    print("4. Entrer le chemin OneDrive dans le champ 'Chemin OneDrive'")
    print("5. Sauvegarder et tester le bouton OneDrive") 