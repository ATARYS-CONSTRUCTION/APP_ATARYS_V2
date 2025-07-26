# -*- coding: utf-8 -*-
"""
SERVICE MAPPING ONEDRIVE → HOSTINGER
===================================

Service pour convertir les chemins OneDrive vers des URLs Hostinger File
Manager

Auteur: ATARYS Team
Date: 2025
"""

import logging
from typing import Optional, Dict
from urllib.parse import quote

logger = logging.getLogger(__name__)


class HostingerPathMapper:
    """Mapping des chemins OneDrive vers Hostinger"""
    
    def __init__(self):
        # Configuration Hostinger
        self.hostinger_ip = "168.231.76.241"
        self.hostinger_base_path = "/home/atarys"
        self.file_manager_base_url = "https://hpanel.hostinger.com/file-manager"
        
        # Mapping des dossiers OneDrive → Hostinger (avec caractères spéciaux)
        self.folder_mapping = {
            "Administration": "Administration",
            "Chantiers": "Chantiers", 
            "Comptabilité 2024": "Comptabilite_2024",
            "Comptabilité 2025": "Comptabilite_2025",
            "Documents Types": "Documents_Types",
            "Images": "Images",
            "Organisation ATARYS": "Organisation_ATARYS",
            "Stavařina": "Stavarina"
        }
        
        # Chemins synchronisés sur Hostinger
        self.synchronized_folders = [
            "Administration",
            "Chantiers", 
            "Comptabilite_2025",
            "Documents_Types",
            "Images",
            "Organisation_ATARYS",
            "Stavarina"
        ]
    
    def is_path_on_hostinger(self, onedrive_relative_path: str) -> bool:
        """
        Vérifie si un chemin OneDrive est synchronisé sur Hostinger
        
        Args:
            onedrive_relative_path: Chemin relatif OneDrive 
                (ex: ./OneDrive/Administration/...)
            
        Returns:
            bool: True si le dossier est synchronisé sur Hostinger
        """
        try:
            # Nettoyer le chemin
            clean_path = self._clean_onedrive_path(onedrive_relative_path)
            
            # Extraire le premier dossier
            path_parts = clean_path.split("/")
            if not path_parts:
                return False
                
            first_folder = path_parts[0]
            
            # Vérifier si le dossier racine est synchronisé
            hostinger_folder = self._map_folder_name(first_folder)
            return hostinger_folder in self.synchronized_folders
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification Hostinger: {e}")
            return False
    
    def convert_to_hostinger_url(self, onedrive_relative_path: str) -> \
            Optional[str]:
        """
        Convertit un chemin OneDrive en URL Hostinger File Manager
        
        Args:
            onedrive_relative_path: Chemin relatif OneDrive
            
        Returns:
            str: URL du File Manager Hostinger ou None si non mappable
        """
        try:
            if not self.is_path_on_hostinger(onedrive_relative_path):
                return None
            
            # Convertir le chemin OneDrive vers Hostinger
            hostinger_path = self._convert_path_to_hostinger(
                onedrive_relative_path)
            
            if not hostinger_path:
                return None
            
            # Générer l'URL du File Manager
            # Note: URL simplifiée - à adapter selon l'interface Hostinger
            encoded_path = quote(hostinger_path)
            url = f"{self.file_manager_base_url}?path={encoded_path}"
            
            return url
            
        except Exception as e:
            logger.error(f"Erreur conversion URL Hostinger: {e}")
            return None
    
    def _clean_onedrive_path(self, path: str) -> str:
        """Nettoie un chemin OneDrive relatif"""
        # Supprimer les préfixes courants
        prefixes_to_remove = [
            "./OneDrive/", "./OneDrive\\", "OneDrive/", "OneDrive\\", "./"
        ]
        
        clean_path = path
        for prefix in prefixes_to_remove:
            if clean_path.startswith(prefix):
                clean_path = clean_path[len(prefix):]
                break
        
        # Normaliser les séparateurs
        clean_path = clean_path.replace("\\", "/")
        
        return clean_path
    
    def _map_folder_name(self, windows_folder_name: str) -> str:
        """Mappe un nom de dossier Windows vers son équivalent Hostinger"""
        return self.folder_mapping.get(windows_folder_name, 
                                        windows_folder_name)
    
    def _convert_path_to_hostinger(self, onedrive_relative_path: str) -> \
            Optional[str]:
        """
        Convertit un chemin OneDrive complet vers un chemin Hostinger
        
        Args:
            onedrive_relative_path: Chemin OneDrive 
                (ex: ./OneDrive/Administration/Volet social/...)
            
        Returns:
            str: Chemin Hostinger 
                (ex: /home/atarys/Administration/Volet social/...)
        """
        try:
            # Nettoyer le chemin
            clean_path = self._clean_onedrive_path(onedrive_relative_path)
            
            if not clean_path:
                return None
            
            # Séparer les parties du chemin
            path_parts = clean_path.split("/")
            
            if not path_parts:
                return None
            
            # Mapper le premier dossier (racine OneDrive)
            first_folder = path_parts[0]
            mapped_first_folder = self._map_folder_name(first_folder)
            
            # Reconstruire le chemin Hostinger
            hostinger_parts = [self.hostinger_base_path, 
                               mapped_first_folder]
            
            # Ajouter les sous-dossiers (sans modification)
            if len(path_parts) > 1:
                hostinger_parts.extend(path_parts[1:])
            
            hostinger_path = "/".join(hostinger_parts)
            
            return hostinger_path
            
        except Exception as e:
            logger.error(f"Erreur conversion chemin Hostinger: {e}")
            return None
    
    def get_mapping_info(self, onedrive_relative_path: str) -> Dict:
        """
        Retourne les informations de mapping pour un chemin OneDrive
        
        Returns:
            dict: Informations détaillées sur le mapping
        """
        return {
            "onedrive_path": onedrive_relative_path,
            "is_on_hostinger": self.is_path_on_hostinger(
                onedrive_relative_path),
            "hostinger_url": self.convert_to_hostinger_url(
                onedrive_relative_path),
            "hostinger_path": self._convert_path_to_hostinger(
                onedrive_relative_path),
            "synchronized_folders": self.synchronized_folders
        }


# Instance globale
hostinger_mapper = HostingerPathMapper() 