#!/usr/bin/env python3
"""
ATARYS - GÉNÉRATEUR DE SCHÉMA DE FORMULAIRE
Script pour générer des schémas de formulaire dynamiques basés sur les modèles SQLAlchemy
"""

import inspect
import re
from app.models.module_5_1 import articlesatarys
from app import db

def analyze_model(model_class):
    """Analyse un modèle SQLAlchemy et génère un schéma de formulaire"""
    
    # Récupérer les colonnes du modèle
    columns = []
    for column_name, column_obj in model_class.__table__.columns.items():
        # Ignorer les colonnes automatiques
        if column_name in ['id', 'created_at', 'updated_at']:
            continue
            
        # Analyser le type de colonne
        column_type = str(column_obj.type)
        nullable = column_obj.nullable
        default = column_obj.default
        
        # Déterminer le type de champ HTML
        field_type = 'text'
        field_validation = {}
        
        if 'Numeric' in column_type:
            field_type = 'number'
            field_validation['step'] = '0.01'
            field_validation['min'] = '0'
        elif 'Integer' in column_type:
            field_type = 'number'
            field_validation['step'] = '1'
        elif 'Boolean' in column_type:
            field_type = 'checkbox'
        elif 'Date' in column_type:
            field_type = 'date'
        elif 'DateTime' in column_type:
            field_type = 'datetime-local'
        elif 'String' in column_type:
            # Extraire la longueur maximale
            match = re.search(r'String\((\d+)\)', column_type)
            if match:
                field_validation['maxlength'] = match.group(1)
            field_type = 'text'
        elif 'Text' in column_type:
            field_type = 'textarea'
        
        # Déterminer si le champ est obligatoire
        required = not nullable
        
        # Suggérer des valeurs par défaut intelligentes
        suggested_default = suggest_default_value(column_name, column_type)
        
        columns.append({
            'name': column_name,
            'type': field_type,
            'required': required,
            'validation': field_validation,
            'default': suggested_default,
            'label': generate_label(column_name)
        })
    
    return columns

def suggest_default_value(column_name, column_type):
    """Suggère des valeurs par défaut intelligentes"""
    suggestions = {
        'actif': True,
        'active': True,
        'enabled': True,
        'visible': True,
        'tva_pct': 20.0,
        'coefficient': 1.0,
        'prix_achat': 0.0,
        'prix_unitaire': 0.0,
        'unite': 'NC',
        'famille': 'Général'
    }
    
    return suggestions.get(column_name, '')

def generate_label(column_name):
    """Génère un label lisible à partir du nom de colonne"""
    # Convertir snake_case en texte lisible
    label = column_name.replace('_', ' ').title()
    
    # Mappings spécifiques
    mappings = {
        'prix_achat': 'Prix d\'achat',
        'prix_unitaire': 'Prix unitaire',
        'tva_pct': 'TVA (%)',
        'date_import': 'Date d\'import',
        'date_maj': 'Date de mise à jour'
    }
    
    return mappings.get(column_name, label)

def generate_form_schema():
    """Génère le schéma de formulaire pour articles_atarys"""
    print("🔍 Analyse du modèle articles_atarys...")
    
    columns = analyze_model(articlesatarys)
    
    print(f"✅ {len(columns)} colonnes analysées")
    
    # Générer le schéma JSON pour le frontend
    schema = {
        'table_name': 'articles_atarys',
        'columns': columns
    }
    
    return schema

if __name__ == "__main__":
    # Créer l'application Flask pour accéder aux modèles
    from app import create_app
    app = create_app()
    
    with app.app_context():
        schema = generate_form_schema()
        
        print("\n📋 Schéma de formulaire généré:")
        print("=" * 50)
        for col in schema['columns']:
            print(f"• {col['name']}: {col['type']} ({'obligatoire' if col['required'] else 'optionnel'})")
            if col['default']:
                print(f"  Valeur par défaut: {col['default']}")
        
        # Sauvegarder le schéma dans un fichier JSON
        import json
        with open('data/form_schema_articles.json', 'w', encoding='utf-8') as f:
            json.dump(schema, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Schéma sauvegardé dans data/form_schema_articles.json") 