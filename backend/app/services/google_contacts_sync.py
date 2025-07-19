#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATARYS - SERVICE SYNCHRONISATION GOOGLE CONTACTS
Service de synchronisation bidirectionnelle avec Google Contacts API

Auteur: ATARYS Team
Date: 2025
Version: 1.0 - Synchronisation bidirectionnelle
"""

import os
import json
import pickle
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from app import db
from app.models.module_2 import Clients  # Table clients ATARYS


class GoogleContactsSync:
    """Service de synchronisation bidirectionnelle avec Google Contacts"""
    
    SCOPES = ['https://www.googleapis.com/auth/contacts']
    
    def __init__(self):
        """Initialiser le service de synchronisation"""
        self.service = None
        self.credentials = None
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data')
        self.token_file = os.path.join(self.data_dir, 'google_contacts_token.pickle')
        self.credentials_file = os.path.join(self.data_dir, 'google_credentials.json')
        
        # Mapping des champs ATARYS ↔ Google Contacts
        self.field_mapping = {
            # ATARYS → Google Contacts
            'nom': 'names.givenName',
            'prenom': 'names.familyName',
            'email': 'emailAddresses.value',
            'telephone': 'phoneNumbers.value',
            'adresse': 'addresses.formattedValue',
            'ville': 'addresses.city',
            'code_postal': 'addresses.postalCode',
            'entreprise': 'organizations.name',
            'fonction': 'organizations.title',
            
            # Google Contacts → ATARYS
            'google_id': 'resourceName',
            'etag': 'etag',
            'last_modified': 'metadata.sources[0].updateTime'
        }
    
    def authenticate(self) -> bool:
        """Authentification OAuth2 avec Google"""
        try:
            creds = None
            
            # Charger les credentials existants
            if os.path.exists(self.token_file):
                with open(self.token_file, 'rb') as token:
                    creds = pickle.load(token)
            
            # Vérifier et rafraîchir si nécessaire
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # Nouvelle authentification
                    if not os.path.exists(self.credentials_file):
                        raise FileNotFoundError(
                            f"Fichier de credentials Google manquant: {self.credentials_file}\n"
                            "Téléchargez-le depuis Google Cloud Console"
                        )
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Sauvegarder les credentials
                with open(self.token_file, 'wb') as token:
                    pickle.dump(creds, token)
            
            self.credentials = creds
            self.service = build('people', 'v1', credentials=creds)
            return True
            
        except Exception as e:
            print(f"❌ Erreur authentification Google: {e}")
            return False
    
    def sync_to_google(self, client_id: int) -> Dict[str, Any]:
        """Synchroniser un client ATARYS vers Google Contacts"""
        try:
            # Récupérer le client depuis ATARYS
            client = Clients.query.get(client_id)
            if not client:
                return {'success': False, 'message': 'Client non trouvé'}
            
            # Préparer les données pour Google Contacts
            contact_data = self._prepare_contact_for_google(client)
            
            # Vérifier si le contact existe déjà
            existing_contact = self._find_contact_by_email(client.email)
            
            if existing_contact:
                # Mettre à jour le contact existant
                result = self.service.people().updateContact(
                    resourceName=existing_contact['resourceName'],
                    body=contact_data
                ).execute()
                action = 'updated'
            else:
                # Créer un nouveau contact
                result = self.service.people().createContact(
                    body=contact_data
                ).execute()
                action = 'created'
            
            # Mettre à jour l'ID Google dans ATARYS
            client.google_id = result['resourceName']
            client.google_etag = result.get('etag', '')
            client.google_last_sync = datetime.utcnow()
            db.session.commit()
            
            return {
                'success': True,
                'message': f'Contact {action} dans Google Contacts',
                'data': {
                    'google_id': result['resourceName'],
                    'action': action
                }
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Erreur sync vers Google: {str(e)}'}
    
    def sync_from_google(self, google_id: str) -> Dict[str, Any]:
        """Synchroniser un contact Google vers ATARYS"""
        try:
            # Récupérer le contact depuis Google
            contact = self.service.people().get(
                resourceName=google_id,
                personFields='names,emailAddresses,phoneNumbers,addresses,organizations'
            ).execute()
            
            # Préparer les données pour ATARYS
            client_data = self._prepare_contact_for_atarys(contact)
            
            # Vérifier si le client existe déjà
            existing_client = Clients.query.filter_by(google_id=google_id).first()
            
            if existing_client:
                # Mettre à jour le client existant
                for field, value in client_data.items():
                    if hasattr(existing_client, field):
                        setattr(existing_client, field, value)
                existing_client.google_last_sync = datetime.utcnow()
                action = 'updated'
            else:
                # Créer un nouveau client
                new_client = Clients(**client_data)
                new_client.google_id = google_id
                new_client.google_last_sync = datetime.utcnow()
                db.session.add(new_client)
                action = 'created'
            
            db.session.commit()
            
            return {
                'success': True,
                'message': f'Client {action} dans ATARYS',
                'data': {
                    'client_id': existing_client.id if existing_client else new_client.id,
                    'action': action
                }
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Erreur sync depuis Google: {str(e)}'}
    
    def sync_all_contacts(self) -> Dict[str, Any]:
        """Synchronisation complète bidirectionnelle"""
        try:
            results = {
                'atarys_to_google': {'success': 0, 'errors': 0},
                'google_to_atarys': {'success': 0, 'errors': 0}
            }
            
            # 1. Synchroniser ATARYS → Google
            clients = Clients.query.all()
            for client in clients:
                if client.email:  # Seulement les clients avec email
                    result = self.sync_to_google(client.id)
                    if result['success']:
                        results['atarys_to_google']['success'] += 1
                    else:
                        results['atarys_to_google']['errors'] += 1
            
            # 2. Synchroniser Google → ATARYS
            contacts = self.service.people().connections().list(
                resourceName='people/me',
                personFields='names,emailAddresses,phoneNumbers,addresses,organizations'
            ).execute()
            
            for contact in contacts.get('connections', []):
                if contact.get('resourceName'):
                    result = self.sync_from_google(contact['resourceName'])
                    if result['success']:
                        results['google_to_atarys']['success'] += 1
                    else:
                        results['google_to_atarys']['errors'] += 1
            
            return {
                'success': True,
                'message': 'Synchronisation complète terminée',
                'data': results
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Erreur sync complète: {str(e)}'}
    
    def _prepare_contact_for_google(self, client) -> Dict[str, Any]:
        """Préparer les données ATARYS pour Google Contacts"""
        contact_data = {
            'names': [{
                'givenName': client.prenom or '',
                'familyName': client.nom or ''
            }],
            'emailAddresses': [{
                'value': client.email or '',
                'type': 'work'
            }] if client.email else [],
            'phoneNumbers': [{
                'value': client.telephone or '',
                'type': 'work'
            }] if client.telephone else [],
            'addresses': [{
                'formattedValue': client.adresse or '',
                'city': client.ville or '',
                'postalCode': client.code_postal or ''
            }] if client.adresse else [],
            'organizations': [{
                'name': client.entreprise or '',
                'title': client.fonction or ''
            }] if client.entreprise else []
        }
        
        return contact_data
    
    def _prepare_contact_for_atarys(self, contact) -> Dict[str, Any]:
        """Préparer les données Google Contacts pour ATARYS"""
        names = contact.get('names', [{}])[0] if contact.get('names') else {}
        emails = contact.get('emailAddresses', [{}])[0] if contact.get('emailAddresses') else {}
        phones = contact.get('phoneNumbers', [{}])[0] if contact.get('phoneNumbers') else {}
        addresses = contact.get('addresses', [{}])[0] if contact.get('addresses') else {}
        organizations = contact.get('organizations', [{}])[0] if contact.get('organizations') else {}
        
        client_data = {
            'nom': names.get('familyName', ''),
            'prenom': names.get('givenName', ''),
            'email': emails.get('value', ''),
            'telephone': phones.get('value', ''),
            'adresse': addresses.get('formattedValue', ''),
            'ville': addresses.get('city', ''),
            'code_postal': addresses.get('postalCode', ''),
            'entreprise': organizations.get('name', ''),
            'fonction': organizations.get('title', '')
        }
        
        return client_data
    
    def _find_contact_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Trouver un contact Google par email"""
        if not email:
            return None
        
        try:
            # Rechercher par email
            results = self.service.people().searchDirectoryPeople(
                query=email,
                readMask='names,emailAddresses'
            ).execute()
            
            for person in results.get('people', []):
                for email_addr in person.get('emailAddresses', []):
                    if email_addr.get('value') == email:
                        return person
            
            return None
            
        except Exception:
            return None


# Instance globale du service
google_contacts_sync = GoogleContactsSync() 