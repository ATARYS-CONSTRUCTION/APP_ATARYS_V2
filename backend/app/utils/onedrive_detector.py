"""
Détecteur OneDrive avec cache intelligent
Gère la détection automatique d'OneDrive sur différents postes Windows
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, List

logger = logging.getLogger(__name__)

class OneDriveDetector:
    """
    Détecteur OneDrive avec cache intelligent pour la portabilité
    """
    
    def __init__(self, cache_file: str = "data/onedrive_cache.json"):
        self.cache_file = cache_file
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """S'assure que le dossier de cache existe"""
        cache_dir = os.path.dirname(self.cache_file)
        if cache_dir and not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)
    
    def get_onedrive_path(self) -> Optional[str]:
        """
        Récupère le chemin OneDrive avec cache intelligent
        
        Returns:
            str: Chemin OneDrive trouvé ou None
        """
        # 1. Essayer le cache d'abord
        cached_path = self._get_cached_path()
        if cached_path and os.path.exists(cached_path):
            logger.info(f"OneDrive trouvé via cache: {cached_path}")
            return cached_path
        
        # 2. Détecter OneDrive sur le système
        detected_path = self._detect_onedrive()
        
        # 3. Sauvegarder si trouvé
        if detected_path:
            self._save_cache(detected_path)
            logger.info(f"OneDrive détecté et sauvegardé: {detected_path}")
        
        return detected_path
    
    def _get_cached_path(self) -> Optional[str]:
        """Récupère le chemin OneDrive depuis le cache"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    cached_path = cache_data.get('onedrive_path')
                    if cached_path and os.path.exists(cached_path):
                        return cached_path
        except Exception as e:
            logger.warning(f"Erreur lors de la lecture du cache: {e}")
        
        return None
    
    def _save_cache(self, onedrive_path: str):
        """Sauvegarde le chemin OneDrive dans le cache"""
        try:
            cache_data = {
                'onedrive_path': onedrive_path,
                'detected_at': str(Path().absolute())
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde du cache: {e}")
    
    def _detect_onedrive(self) -> Optional[str]:
        """
        Détecte automatiquement OneDrive sur le système Windows
        
        Returns:
            str: Premier chemin OneDrive trouvé ou None
        """
        # Liste des emplacements OneDrive possibles (par ordre de priorité)
        possible_locations = [
            # 1. Variable d'environnement personnalisée
            os.environ.get('ONEDRIVE_PATH'),
            
            # 2. OneDrive personnel (le plus courant)
            os.path.expanduser('~/OneDrive'),
            os.path.expanduser('~/OneDrive - ATARYS'),
            
            # 3. OneDrive dans Documents
            os.path.expanduser('~/Documents/OneDrive'),
            
            # 4. OneDrive sur lecteurs alternatifs
            'C:/OneDrive',
            'D:/OneDrive',
            'E:/OneDrive',
            
            # 5. OneDrive public
            'C:/Users/Public/OneDrive',
            
            # 6. OneDrive dans le profil utilisateur
            os.path.expanduser('~/AppData/Local/Microsoft/OneDrive'),
            
            # 7. OneDrive dans le profil utilisateur Windows
            os.path.join(os.environ.get('USERPROFILE', ''), 'OneDrive'),
            os.path.join(os.environ.get('USERPROFILE', ''), 'OneDrive - ATARYS'),
        ]
        
        # Filtrer les chemins None et tester l'existence
        valid_locations = [loc for loc in possible_locations if loc]
        
        logger.info(f"Recherche OneDrive dans {len(valid_locations)} emplacements...")
        
        for location in valid_locations:
            try:
                if os.path.exists(location):
                    logger.info(f"OneDrive trouvé: {location}")
                    return location
            except Exception as e:
                logger.warning(f"Erreur lors du test de {location}: {e}")
        
        logger.warning("Aucun OneDrive trouvé sur le système")
        return None
    
    def resolve_relative_path(self, relative_path: str) -> Optional[str]:
        """
        Résout un chemin relatif OneDrive vers un chemin absolu
        
        Args:
            relative_path: Chemin relatif (ex: "./OneDrive/Admin/Salariés/Dupont")
            
        Returns:
            str: Chemin absolu résolu ou None
        """
        # 1. Nettoyer le chemin relatif
        clean_relative = relative_path.strip()
        
        # 2. Enlever "./" ou ".\" si présent
        if clean_relative.startswith('./') or clean_relative.startswith('.\\'):
            clean_relative = clean_relative[2:]
        
        # 3. Normaliser les séparateurs
        clean_relative = clean_relative.replace('/', '\\')
        
        # 4. Trouver OneDrive
        onedrive_base = self.get_onedrive_path()
        if not onedrive_base:
            logger.error("OneDrive non trouvé sur le système")
            return None
        
        # 5. CORRECTION : Enlever "OneDrive" du début du chemin relatif si présent
        # pour éviter la duplication
        if clean_relative.lower().startswith('onedrive\\'):
            clean_relative = clean_relative[9:]  # Enlever "OneDrive\"
        elif clean_relative.lower().startswith('onedrive/'):
            clean_relative = clean_relative[9:]  # Enlever "OneDrive/"
        
        # 6. Construire le chemin complet
        full_path = os.path.join(onedrive_base, clean_relative)
        
        logger.info(f"Chemin résolu: {full_path}")
        return full_path
    
    def test_path(self, relative_path: str) -> dict:
        """
        Teste un chemin relatif OneDrive
        
        Args:
            relative_path: Chemin relatif à tester
            
        Returns:
            dict: Résultat du test avec statut et informations
        """
        try:
            resolved_path = self.resolve_relative_path(relative_path)
            
            if not resolved_path:
                return {
                    'success': False,
                    'error': 'OneDrive non trouvé sur le système',
                    'relative_path': relative_path,
                    'resolved_path': None
                }
            
            exists = os.path.exists(resolved_path)
            
            return {
                'success': True,
                'exists': exists,
                'relative_path': relative_path,
                'resolved_path': resolved_path,
                'onedrive_base': self.get_onedrive_path(),
                'message': 'Dossier trouvé' if exists else 'Dossier non trouvé'
            }
            
        except Exception as e:
            logger.error(f"Erreur lors du test du chemin: {e}")
            return {
                'success': False,
                'error': str(e),
                'relative_path': relative_path,
                'resolved_path': None
            }
    
    def clear_cache(self):
        """Efface le cache OneDrive"""
        try:
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
                logger.info("Cache OneDrive effacé")
        except Exception as e:
            logger.error(f"Erreur lors de l'effacement du cache: {e}")
    
    def get_detection_info(self) -> dict:
        """
        Retourne les informations de détection OneDrive
        
        Returns:
            dict: Informations sur la détection
        """
        cached_path = self._get_cached_path()
        detected_path = self._detect_onedrive()
        
        return {
            'cached_path': cached_path,
            'cached_exists': cached_path and os.path.exists(cached_path),
            'detected_path': detected_path,
            'cache_file': self.cache_file,
            'cache_exists': os.path.exists(self.cache_file)
        }


# Instance globale pour réutilisation
onedrive_detector = OneDriveDetector() 