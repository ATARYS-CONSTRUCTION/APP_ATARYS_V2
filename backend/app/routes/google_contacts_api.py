#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - ROUTES API SYNCHRONISATION GOOGLE CONTACTS
Routes pour la synchronisation bidirectionnelle avec Google Contacts

Auteur: ATARYS Team
Date: 2025
Version: 1.0 - API de synchronisation
"""

from flask import Blueprint, jsonify, request
from app.services.google_contacts_sync import google_contacts_sync

google_contacts_bp = Blueprint('google_contacts', __name__)


@google_contacts_bp.route('/api/google-contacts/auth', methods=['POST'])
def authenticate_google():
    """Authentifier avec Google Contacts"""
    try:
        success = google_contacts_sync.authenticate()
        
        if success:
            return jsonify({
                'success': True,
                'message': '✅ Authentification Google réussie',
                'data': {
                    'authenticated': True,
                    'service_available': google_contacts_sync.service is not None
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': '❌ Échec de l\'authentification Google'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur authentification: {str(e)}'
        }), 500


@google_contacts_bp.route('/api/google-contacts/sync-to-google/<int:client_id>', methods=['POST'])
def sync_client_to_google(client_id):
    """Synchroniser un client ATARYS vers Google Contacts"""
    try:
        # Vérifier l'authentification
        if not google_contacts_sync.service:
            if not google_contacts_sync.authenticate():
                return jsonify({
                    'success': False,
                    'message': '❌ Authentification Google requise'
                }), 401
        
        result = google_contacts_sync.sync_to_google(client_id)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur sync vers Google: {str(e)}'
        }), 500


@google_contacts_bp.route('/api/google-contacts/sync-from-google/<google_id>', methods=['POST'])
def sync_contact_from_google(google_id):
    """Synchroniser un contact Google vers ATARYS"""
    try:
        # Vérifier l'authentification
        if not google_contacts_sync.service:
            if not google_contacts_sync.authenticate():
                return jsonify({
                    'success': False,
                    'message': '❌ Authentification Google requise'
                }), 401
        
        result = google_contacts_sync.sync_from_google(google_id)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur sync depuis Google: {str(e)}'
        }), 500


@google_contacts_bp.route('/api/google-contacts/sync-all', methods=['POST'])
def sync_all_contacts():
    """Synchronisation complète bidirectionnelle"""
    try:
        # Vérifier l'authentification
        if not google_contacts_sync.service:
            if not google_contacts_sync.authenticate():
                return jsonify({
                    'success': False,
                    'message': '❌ Authentification Google requise'
                }), 401
        
        result = google_contacts_sync.sync_all_contacts()
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur sync complète: {str(e)}'
        }), 500


@google_contacts_bp.route('/api/google-contacts/status', methods=['GET'])
def get_sync_status():
    """Obtenir le statut de la synchronisation"""
    try:
        authenticated = google_contacts_sync.service is not None
        
        return jsonify({
            'success': True,
            'data': {
                'authenticated': authenticated,
                'service_available': google_contacts_sync.service is not None,
                'credentials_file_exists': google_contacts_sync.credentials_file is not None,
                'token_file_exists': google_contacts_sync.token_file is not None
            },
            'message': '✅ Service Google Contacts disponible' if authenticated else '❌ Authentification requise'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur statut: {str(e)}'
        }), 500


@google_contacts_bp.route('/api/google-contacts/list-contacts', methods=['GET'])
def list_google_contacts():
    """Lister tous les contacts Google"""
    try:
        # Vérifier l'authentification
        if not google_contacts_sync.service:
            if not google_contacts_sync.authenticate():
                return jsonify({
                    'success': False,
                    'message': '❌ Authentification Google requise'
                }), 401
        
        # Récupérer les contacts
        contacts = google_contacts_sync.service.people().connections().list(
            resourceName='people/me',
            personFields='names,emailAddresses,phoneNumbers,addresses,organizations',
            pageSize=100
        ).execute()
        
        contact_list = []
        for contact in contacts.get('connections', []):
            names = contact.get('names', [{}])[0] if contact.get('names') else {}
            emails = contact.get('emailAddresses', [{}])[0] if contact.get('emailAddresses') else {}
            
            contact_list.append({
                'google_id': contact.get('resourceName'),
                'nom': names.get('familyName', ''),
                'prenom': names.get('givenName', ''),
                'email': emails.get('value', ''),
                'etag': contact.get('etag', '')
            })
        
        return jsonify({
            'success': True,
            'data': contact_list,
            'message': f'{len(contact_list)} contacts trouvés dans Google'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur liste contacts: {str(e)}'
        }), 500


@google_contacts_bp.route('/api/google-contacts/setup-instructions', methods=['GET'])
def get_setup_instructions():
    """Obtenir les instructions de configuration Google Contacts"""
    instructions = {
        'success': True,
        'data': {
            'steps': [
                {
                    'step': 1,
                    'title': 'Créer un projet Google Cloud',
                    'description': 'Allez sur https://console.cloud.google.com et créez un nouveau projet',
                    'url': 'https://console.cloud.google.com'
                },
                {
                    'step': 2,
                    'title': 'Activer l\'API Google People',
                    'description': 'Dans votre projet, activez l\'API "Google People API"',
                    'url': 'https://console.cloud.google.com/apis/library/people.googleapis.com'
                },
                {
                    'step': 3,
                    'title': 'Créer des credentials OAuth2',
                    'description': 'Créez des credentials OAuth2 pour une application de bureau',
                    'url': 'https://console.cloud.google.com/apis/credentials'
                },
                {
                    'step': 4,
                    'title': 'Télécharger le fichier JSON',
                    'description': 'Téléchargez le fichier JSON des credentials et placez-le dans data/google_credentials.json',
                    'file_path': 'data/google_credentials.json'
                },
                {
                    'step': 5,
                    'title': 'Authentifier l\'application',
                    'description': 'Utilisez l\'endpoint /api/google-contacts/auth pour l\'authentification initiale',
                    'endpoint': '/api/google-contacts/auth'
                }
            ],
            'required_files': [
                'data/google_credentials.json'
            ],
            'scopes': [
                'https://www.googleapis.com/auth/contacts'
            ]
        },
        'message': 'Instructions de configuration Google Contacts'
    }
    
    return jsonify(instructions) 