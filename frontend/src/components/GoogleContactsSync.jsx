import React, { useState, useEffect } from 'react';

const GoogleContactsSync = () => {
  const [syncStatus, setSyncStatus] = useState('idle');
  const [authStatus, setAuthStatus] = useState(null);
  const [syncResults, setSyncResults] = useState(null);
  const [loading, setLoading] = useState(false);

  // Vérifier le statut d'authentification au chargement
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await fetch('/api/google-contacts/status');
      const result = await response.json();
      setAuthStatus(result.data);
    } catch (error) {
      console.error('Erreur vérification statut:', error);
    }
  };

  const handleAuthenticate = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/google-contacts/auth', {
        method: 'POST'
      });
      const result = await response.json();
      
      if (result.success) {
        setAuthStatus(result.data);
        setSyncStatus('authenticated');
      } else {
        setSyncStatus('auth_error');
      }
    } catch (error) {
      setSyncStatus('error');
      console.error('Erreur authentification:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSyncAll = async () => {
    setLoading(true);
    setSyncStatus('syncing');
    
    try {
      const response = await fetch('/api/google-contacts/sync-all', {
        method: 'POST'
      });
      const result = await response.json();
      
      if (result.success) {
        setSyncResults(result.data);
        setSyncStatus('success');
      } else {
        setSyncStatus('sync_error');
      }
    } catch (error) {
      setSyncStatus('error');
      console.error('Erreur synchronisation:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGetInstructions = async () => {
    try {
      const response = await fetch('/api/google-contacts/setup-instructions');
      const result = await response.json();
      
      if (result.success) {
        // Afficher les instructions dans une modal ou nouvelle fenêtre
        const instructions = result.data.steps.map(step => 
          `${step.step}. ${step.title}: ${step.description}`
        ).join('\n');
        
        alert('Instructions de configuration:\n\n' + instructions);
      }
    } catch (error) {
      console.error('Erreur récupération instructions:', error);
    }
  };

  const getStatusColor = () => {
    switch (syncStatus) {
      case 'success': return 'text-green-600';
      case 'error': return 'text-red-600';
      case 'syncing': return 'text-blue-600';
      case 'auth_error': return 'text-orange-600';
      default: return 'text-gray-600';
    }
  };

  const getStatusText = () => {
    switch (syncStatus) {
      case 'idle': return 'En attente';
      case 'authenticated': return 'Authentifié';
      case 'syncing': return 'Synchronisation en cours...';
      case 'success': return 'Synchronisation réussie';
      case 'error': return 'Erreur de synchronisation';
      case 'auth_error': return 'Erreur d\'authentification';
      default: return 'Statut inconnu';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        🔗 Synchronisation Google Contacts
      </h2>

      {/* Statut d'authentification */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-3">
          Statut d'authentification
        </h3>
        
        {authStatus ? (
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${
                authStatus.authenticated ? 'bg-green-500' : 'bg-red-500'
              }`}></div>
              <span className="text-sm">
                {authStatus.authenticated ? '✅ Authentifié' : '❌ Non authentifié'}
              </span>
            </div>
            
            <div className="text-xs text-gray-500 space-y-1">
              <div>Service disponible: {authStatus.service_available ? '✅' : '❌'}</div>
              <div>Fichier credentials: {authStatus.credentials_file_exists ? '✅' : '❌'}</div>
              <div>Token sauvegardé: {authStatus.token_file_exists ? '✅' : '❌'}</div>
            </div>
          </div>
        ) : (
          <div className="text-gray-500">Chargement du statut...</div>
        )}
      </div>

      {/* Actions */}
      <div className="space-y-4">
        {!authStatus?.authenticated ? (
          <div className="space-y-3">
            <button
              onClick={handleAuthenticate}
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition-colors"
            >
              {loading ? 'Authentification...' : '🔐 S\'authentifier avec Google'}
            </button>
            
            <button
              onClick={handleGetInstructions}
              className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg transition-colors"
            >
              📋 Voir les instructions de configuration
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            <button
              onClick={handleSyncAll}
              disabled={loading}
              className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition-colors"
            >
              {loading ? 'Synchronisation...' : '🔄 Synchroniser tous les contacts'}
            </button>
            
            <div className="text-sm text-gray-600">
              Synchronise bidirectionnellement ATARYS ↔ Google Contacts
            </div>
          </div>
        )}
      </div>

      {/* Statut de synchronisation */}
      {syncStatus !== 'idle' && (
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <div className="flex items-center space-x-2 mb-2">
            <div className={`w-3 h-3 rounded-full ${
              syncStatus === 'success' ? 'bg-green-500' : 
              syncStatus === 'error' ? 'bg-red-500' : 'bg-blue-500'
            }`}></div>
            <span className={`font-medium ${getStatusColor()}`}>
              {getStatusText()}
            </span>
          </div>
          
          {syncResults && (
            <div className="text-sm text-gray-600 space-y-1">
              <div>ATARYS → Google: {syncResults.atarys_to_google.success} succès, {syncResults.atarys_to_google.errors} erreurs</div>
              <div>Google → ATARYS: {syncResults.google_to_atarys.success} succès, {syncResults.google_to_atarys.errors} erreurs</div>
            </div>
          )}
        </div>
      )}

      {/* Informations */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h4 className="font-semibold text-blue-800 mb-2">ℹ️ Informations</h4>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>• Synchronisation bidirectionnelle automatique</li>
          <li>• Utilise l'email comme clé unique</li>
          <li>• Gestion automatique des conflits</li>
          <li>• Sauvegarde des tokens d'authentification</li>
        </ul>
      </div>
    </div>
  );
};

export default GoogleContactsSync; 