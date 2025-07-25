import React, { useState, useEffect } from 'react';
import { PageLayout } from '../components/Layout';

const Module9_1 = () => {
  const [salaries, setSalaries] = useState([]);
  const [niveauQualifications, setNiveauQualifications] = useState([]);
  const [familleOuvrages, setFamilleOuvrages] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingSalary, setEditingSalary] = useState(null);
  const [showInactifs, setShowInactifs] = useState(false);
  const [selectedSalary, setSelectedSalary] = useState(null);
  
  const [formData, setFormData] = useState({
    nom: '',
    prenom: '',
    salaire_brut_horaire: '',
    nbre_heure_hebdo: '',
    type_contrat: '',
    date_entree: '',
    date_sortie: '',
    niveau_qualification_id: '',
    colonne_planning: '',
    email: '',
    num_telephone: '',
    adresse: '',
    ville_id: '', // MIS À JOUR : remplace code_postal et ville
    date_naissance: '',
    num_securite_social: '',
    ondrive_path: '',
    famille_ouvrages_ids: []
  });

  // États pour l'autocomplétion des villes
  const [villes, setVilles] = useState([]);
  const [villeSearch, setVilleSearch] = useState('');
  const [showVilleDropdown, setShowVilleDropdown] = useState(false);

  useEffect(() => {
    fetchSalaries();
    fetchNiveauQualifications();
    fetchFamilleOuvrages();
    fetchVilles(); // AJOUTÉ : charger les villes
  }, []);

  const fetchSalaries = async () => {
    try {
      const response = await fetch('/api/salaries/');
      const data = await response.json();
      if (data.success) {
        setSalaries(data.data);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des salariés:', error);
    }
  };

  const fetchNiveauQualifications = async () => {
    try {
      const response = await fetch('/api/niveau_qualification/');
      const data = await response.json();
      if (data.success) {
        setNiveauQualifications(data.data);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des niveaux de qualification:', error);
    }
  };

  const fetchFamilleOuvrages = async () => {
    try {
      const response = await fetch('/api/famille_ouvrages/');
      const data = await response.json();
      if (data.success) {
        setFamilleOuvrages(data.data);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des familles d\'ouvrages:', error);
    }
  };

  // AJOUTÉ : Fonction pour charger les villes
  const fetchVilles = async () => {
    try {
      const response = await fetch('/api/villes/');
      const data = await response.json();
      if (data.success) {
        setVilles(data.data);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des villes:', error);
    }
  };

  // AJOUTÉ : Fonction pour rechercher des villes
  const searchVilles = async (query) => {
    try {
      const response = await fetch(`/api/villes/search?ville=${encodeURIComponent(query)}`);
      const data = await response.json();
      if (data.success) {
        setVilles(data.data);
        setShowVilleDropdown(true);
      }
    } catch (error) {
      console.error('Erreur lors de la recherche de villes:', error);
    }
  };

  // AJOUTÉ : Fonction pour sélectionner une ville
  const selectVille = (ville) => {
    setFormData({ ...formData, ville_id: ville.id });
    setVilleSearch(`${ville.communes} (${ville.code_postal})`);
    setShowVilleDropdown(false);
  };

  // AJOUTÉ : Gestionnaire pour fermer le dropdown
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (showVilleDropdown && !event.target.closest('.relative')) {
        setShowVilleDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showVilleDropdown]);

  // Fonction pour filtrer les salariés actifs/inactifs
  const getFilteredSalaries = () => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    return salaries.filter(salary => {
      if (salary.date_sortie) {
        const dateSortie = new Date(salary.date_sortie);
        const isInactif = dateSortie < today;
        return showInactifs ? isInactif : !isInactif;
      }
      // Si pas de date de sortie, considérer comme actif
      return !showInactifs;
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      // Validation des données avant envoi
      const dataToSend = { ...formData };
      
      // Nettoyer les champs vides
      Object.keys(dataToSend).forEach(key => {
        if (dataToSend[key] === '' || dataToSend[key] === null || dataToSend[key] === undefined) {
          // Ne pas envoyer les champs vides pour type_contrat et autres champs optionnels
          if (key === 'type_contrat' || key === 'date_sortie' || key === 'email' || 
              key === 'num_telephone' || key === 'adresse' || key === 'ville_id' || // MIS À JOUR
              key === 'date_naissance' || key === 'num_securite_social' || 
              key === 'ondrive_path' || key === 'niveau_qualification_id' || key === 'colonne_planning' ||
              key === 'famille_ouvrages_ids') {
            dataToSend[key] = null;
          }
        }
      });
      
      // Validation spécifique pour les champs numériques
      if (dataToSend.salaire_brut_horaire && !isNaN(dataToSend.salaire_brut_horaire)) {
        dataToSend.salaire_brut_horaire = parseFloat(dataToSend.salaire_brut_horaire);
      }
      
      if (dataToSend.nbre_heure_hebdo && !isNaN(dataToSend.nbre_heure_hebdo)) {
        dataToSend.nbre_heure_hebdo = parseFloat(dataToSend.nbre_heure_hebdo);
      }
      
      if (dataToSend.niveau_qualification_id && !isNaN(dataToSend.niveau_qualification_id)) {
        dataToSend.niveau_qualification_id = parseInt(dataToSend.niveau_qualification_id);
      }
      
      console.log('Données à envoyer:', dataToSend);
      
      const url = editingSalary 
        ? `/api/salaries/${editingSalary.id}` 
        : '/api/salaries/';
      
      const method = editingSalary ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend),
      });

      const result = await response.json();
      
      if (result.success) {
        setShowModal(false);
        setEditingSalary(null);
        setFormData({
          nom: '',
          prenom: '',
          salaire_brut_horaire: '',
          nbre_heure_hebdo: '',
          type_contrat: '',
          date_entree: '',
          date_sortie: '',
          niveau_qualification_id: '',
          colonne_planning: '',
          email: '',
          num_telephone: '',
          adresse: '',
          ville_id: '', // MIS À JOUR
          date_naissance: '',
          num_securite_social: '',
          ondrive_path: '',
          famille_ouvrages_ids: []
        });
        setVilleSearch(''); // AJOUTÉ : réinitialiser la recherche de ville
        fetchSalaries();
      } else {
        console.error('Erreur API:', result);
        alert('Erreur: ' + (result.message || 'Erreur inconnue'));
      }
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error);
      alert('Erreur lors de la sauvegarde: ' + error.message);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce salarié ?')) {
      try {
        const response = await fetch(`/api/salaries/${id}`, {
          method: 'DELETE',
        });
        
        const result = await response.json();
        
        if (result.success) {
          fetchSalaries();
          alert('Salarié supprimé avec succès');
        } else {
          alert('Erreur lors de la suppression: ' + result.message);
        }
      } catch (error) {
        console.error('Erreur lors de la suppression:', error);
        alert('Erreur lors de la suppression');
      }
    }
  };

  const handleRowClick = (salary) => {
    setSelectedSalary(salary);
  };

  const handleOneDrive = async (salary) => {
    if (!salary.ondrive_path) {
      alert('Aucun chemin OneDrive configuré pour ce salarié.');
      return;
    }

    try {
      console.log('Chemin OneDrive relatif à ouvrir:', salary.ondrive_path);
      
      const response = await fetch('/api/open-explorer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          path: salary.ondrive_path
        }),
      });

      const result = await response.json();
      
      if (result.success) {
        console.log('Dossier OneDrive ouvert avec succès');
        console.log('Chemin résolu:', result.resolved_path);
      } else {
        console.error('Erreur lors de l\'ouverture du dossier:', result.message);
        alert('Erreur lors de l\'ouverture du dossier: ' + result.message);
      }
    } catch (error) {
      console.error('Erreur lors de l\'ouverture OneDrive:', error);
      alert('Erreur lors de l\'ouverture du dossier OneDrive');
    }
  };

  const testOneDrivePath = async (path) => {
    try {
      const response = await fetch('/api/test-onedrive-path', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ path }),
      });

      return await response.json();
    } catch (error) {
      console.error('Erreur lors du test OneDrive:', error);
      return { success: false, error: error.message };
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('fr-FR');
  };

  const formatCurrency = (amount) => {
    if (!amount) return '-';
    return `${parseFloat(amount).toFixed(2)}€`;
  };

  const filteredSalaries = getFilteredSalaries();

  return (
    <PageLayout variant="ultrawide" title="LISTE_SALARIES">
      <div className="space-y-4">
        {/* Filtres et boutons */}
        <div className="flex flex-wrap gap-4 items-center justify-between p-2">
          <div className="flex items-center gap-4">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={showInactifs}
                onChange={(e) => setShowInactifs(e.target.checked)}
                className="rounded"
              />
              <span className="text-sm font-medium">Afficher les inactifs</span>
            </label>
          </div>
          
          <div className="flex gap-2">
            <button
              onClick={() => {
                setEditingSalary(null);
                setFormData({
                  nom: '',
                  prenom: '',
                  salaire_brut_horaire: '',
                  nbre_heure_hebdo: '',
                  type_contrat: '',
                  date_entree: '',
                  date_sortie: '',
                  niveau_qualification_id: '',
                  colonne_planning: '',
                  email: '',
                  num_telephone: '',
                  adresse: '',
                  code_postal: '',
                  ville: '',
                  date_naissance: '',
                  num_securite_social: '',
                  ondrive_path: '',
                  famille_ouvrages_ids: []
                });
                setShowModal(true);
              }}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium"
            >
              CREER SALARIES
            </button>
            
            <button
              onClick={() => {
                if (selectedSalary) {
                  setEditingSalary(selectedSalary);
                  setFormData({
                    nom: selectedSalary.nom || '',
                    prenom: selectedSalary.prenom || '',
                    salaire_brut_horaire: selectedSalary.salaire_brut_horaire || '',
                    nbre_heure_hebdo: selectedSalary.nbre_heure_hebdo || '',
                    type_contrat: selectedSalary.type_contrat || '',
                    date_entree: selectedSalary.date_entree || '',
                    date_sortie: selectedSalary.date_sortie || '',
                    niveau_qualification_id: selectedSalary.niveau_qualification_id || '',
                    colonne_planning: selectedSalary.colonne_planning || '',
                    email: selectedSalary.email || '',
                    num_telephone: selectedSalary.num_telephone || '',
                    adresse: selectedSalary.adresse || '',
                    code_postal: selectedSalary.code_postal || '',
                    ville: selectedSalary.ville || '',
                    date_naissance: selectedSalary.date_naissance || '',
                    num_securite_social: selectedSalary.num_securite_social || '',
                    ondrive_path: selectedSalary.ondrive_path || '',
                    famille_ouvrages_ids: selectedSalary.famille_ouvrages_ids || []
                  });
                  setShowModal(true);
                } else {
                  alert('Veuillez sélectionner un salarié à modifier');
                }
              }}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-medium"
            >
              MODIFIER SALARIES
            </button>
            
            <button
              onClick={() => {
                if (selectedSalary) {
                  handleOneDrive(selectedSalary);
                } else {
                  alert('Veuillez sélectionner un salarié pour ouvrir OneDrive');
                }
              }}
              className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg font-medium"
            >
              ONEDRIVE
            </button>
          </div>
        </div>

        {/* Tableau des salariés */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Nom</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Prénom</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Salaire/H</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Heures/Sem</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Contrat</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Entrée</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Sortie</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Qualification</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Planning</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Email</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Téléphone</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Adresse</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Code postal</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Ville</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Date naissance</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">N° Sécurité sociale</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Familles d'ouvrages</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">OneDrive</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-700">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {filteredSalaries.map((salary) => (
                  <tr
                    key={salary.id}
                    onClick={() => handleRowClick(salary)}
                    onDoubleClick={() => {
                      setEditingSalary(salary);
                      setFormData({
                        nom: salary.nom || '',
                        prenom: salary.prenom || '',
                        salaire_brut_horaire: salary.salaire_brut_horaire || '',
                        nbre_heure_hebdo: salary.nbre_heure_hebdo || '',
                        type_contrat: salary.type_contrat || '',
                        date_entree: salary.date_entree || '',
                        date_sortie: salary.date_sortie || '',
                        niveau_qualification_id: salary.niveau_qualification_id || '',
                        colonne_planning: salary.colonne_planning || '',
                        email: salary.email || '',
                        num_telephone: salary.num_telephone || '',
                        adresse: salary.adresse || '',
                        ville_id: salary.ville_id || '',
                        date_naissance: salary.date_naissance || '',
                        num_securite_social: salary.num_securite_social || '',
                        ondrive_path: salary.ondrive_path || '',
                        famille_ouvrages_ids: salary.famille_ouvrages_ids || []
                      });
                      // AJOUTÉ : Mettre à jour la recherche de ville
                      if (salary.ville) {
                        setVilleSearch(`${salary.ville.communes} (${salary.ville.code_postal})`);
                      } else {
                        setVilleSearch('');
                      }
                      setShowModal(true);
                    }}
                    className={`hover:bg-gray-50 cursor-pointer transition-colors duration-150 ${
                      selectedSalary?.id === salary.id ? 'bg-blue-50 border-l-4 border-blue-500' : ''
                    }`}
                  >
                    <td className="px-3 py-2">{salary.nom}</td>
                    <td className="px-3 py-2">{salary.prenom}</td>
                    <td className="px-3 py-2">{formatCurrency(salary.salaire_brut_horaire)}</td>
                    <td className="px-3 py-2">{salary.nbre_heure_hebdo}</td>
                    <td className="px-3 py-2">{salary.type_contrat || '-'}</td>
                    <td className="px-3 py-2">{formatDate(salary.date_entree)}</td>
                    <td className="px-3 py-2">{formatDate(salary.date_sortie)}</td>
                    <td className="px-3 py-2">
                      {niveauQualifications.find(q => q.id === salary.niveau_qualification_id)?.niveau || '-'}
                    </td>
                    <td className="px-3 py-2">
                      {salary.colonne_planning || '-'}
                    </td>
                    <td className="px-3 py-2">
                      {salary.email || '-'}
                    </td>
                    <td className="px-3 py-2">
                      {salary.num_telephone || '-'}
                    </td>
                    <td className="px-3 py-2">
                      {salary.adresse || '-'}
                    </td>
                    <td className="px-3 py-2">
                      {salary.ville && salary.ville.code_postal ? salary.ville.code_postal : '-'}
                    </td>
                    <td className="px-3 py-2">
                      {salary.ville && salary.ville.communes ? salary.ville.communes : '-'}
                    </td>
                    <td className="px-3 py-2">
                      {formatDate(salary.date_naissance) || '-'}
                    </td>
                    <td className="px-3 py-2">
                      {salary.num_securite_social || '-'}
                    </td>
                    <td className="px-3 py-2">
                      {salary.famille_ouvrages && salary.famille_ouvrages.length > 0 
                        ? salary.famille_ouvrages.map(fo => fo.num_bd_atarys || fo.libelle).join(', ')
                        : '-'
                      }
                    </td>
                    <td className="px-3 py-2">
                      {salary.ondrive_path && (
                        <span className="text-xs text-gray-500 truncate max-w-32 block">
                          {salary.ondrive_path}
                        </span>
                      )}
                    </td>
                    <td className="px-3 py-2">
                      <div className="flex gap-1">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setEditingSalary(salary);
                            setFormData({
                              nom: salary.nom || '',
                              prenom: salary.prenom || '',
                              salaire_brut_horaire: salary.salaire_brut_horaire || '',
                              nbre_heure_hebdo: salary.nbre_heure_hebdo || '',
                              type_contrat: salary.type_contrat || '',
                              date_entree: salary.date_entree || '',
                              date_sortie: salary.date_sortie || '',
                              niveau_qualification_id: salary.niveau_qualification_id || '',
                              colonne_planning: salary.colonne_planning || '',
                              email: salary.email || '',
                              num_telephone: salary.num_telephone || '',
                              adresse: salary.adresse || '',
                              code_postal: salary.code_postal || '',
                              ville: salary.ville || '',
                              date_naissance: salary.date_naissance || '',
                              num_securite_social: salary.num_securite_social || '',
                              ondrive_path: salary.ondrive_path || '',
                              famille_ouvrages_ids: salary.famille_ouvrages_ids || []
                            });
                            setShowModal(true);
                          }}
                          className="bg-blue-500 hover:bg-blue-600 text-white px-2 py-1 rounded text-xs"
                        >
                          Modifier
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDelete(salary.id);
                          }}
                          className="bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded text-xs"
                        >
                          Supprimer
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleOneDrive(salary);
                          }}
                          className="bg-purple-500 hover:bg-purple-600 text-white px-2 py-1 rounded text-xs"
                        >
                          OneDrive
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

        {/* Modal pour créer/modifier un salarié */}
        {showModal && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  {editingSalary ? 'Modifier le salarié' : 'Créer un nouveau salarié'}
                </h3>
                
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Nom *</label>
                      <input
                        type="text"
                        value={formData.nom}
                        onChange={(e) => setFormData({...formData, nom: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                        required
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Prénom *</label>
                      <input
                        type="text"
                        value={formData.prenom}
                        onChange={(e) => setFormData({...formData, prenom: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                        required
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Salaire brut horaire</label>
                      <input
                        type="number"
                        step="0.01"
                        value={formData.salaire_brut_horaire}
                        onChange={(e) => setFormData({...formData, salaire_brut_horaire: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Nombre d'heures hebdomadaires</label>
                      <input
                        type="number"
                        step="0.01"
                        value={formData.nbre_heure_hebdo}
                        onChange={(e) => setFormData({...formData, nbre_heure_hebdo: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Type de contrat</label>
                      <select
                        value={formData.type_contrat}
                        onChange={(e) => setFormData({...formData, type_contrat: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      >
                        <option value="">Sélectionner...</option>
                        <option value="CDI">CDI</option>
                        <option value="CDD">CDD</option>
                        <option value="Apprentissage">Apprentissage</option>
                        <option value="INTERIM">INTERIM</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Date d'entrée *</label>
                      <input
                        type="date"
                        value={formData.date_entree}
                        onChange={(e) => setFormData({...formData, date_entree: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Date de sortie</label>
                      <input
                        type="date"
                        value={formData.date_sortie}
                        onChange={(e) => setFormData({...formData, date_sortie: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Niveau de qualification</label>
                      <select
                        value={formData.niveau_qualification_id}
                        onChange={(e) => setFormData({...formData, niveau_qualification_id: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      >
                        <option value="">Sélectionner...</option>
                        {niveauQualifications.map((niveau) => (
                          <option key={niveau.id} value={niveau.id}>
                            {niveau.niveau}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Colonne planning</label>
                      <input
                        type="text"
                        value={formData.colonne_planning}
                        onChange={(e) => setFormData({...formData, colonne_planning: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Email</label>
                      <input
                        type="email"
                        value={formData.email}
                        onChange={(e) => setFormData({...formData, email: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Numéro de téléphone</label>
                      <input
                        type="tel"
                        value={formData.num_telephone}
                        onChange={(e) => setFormData({...formData, num_telephone: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Adresse</label>
                      <input
                        type="text"
                        value={formData.adresse}
                        onChange={(e) => setFormData({...formData, adresse: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      />
                    </div>
                    <div className="relative">
                      <label className="block text-sm font-medium text-gray-700">Ville</label>
                      <input
                        type="text"
                        value={villeSearch}
                        onChange={(e) => {
                          const query = e.target.value;
                          setVilleSearch(query);
                          if (query.length >= 2) {
                            searchVilles(query);
                          } else {
                            setShowVilleDropdown(false);
                          }
                        }}
                        onFocus={() => {
                          if (villeSearch.length >= 2) {
                            setShowVilleDropdown(true);
                          }
                        }}
                        placeholder="Tapez le nom de la ville ou le code postal..."
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      />
                      {showVilleDropdown && villes.length > 0 && (
                        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
                          {villes.map((ville) => (
                            <div
                              key={ville.id}
                              onClick={() => selectVille(ville)}
                              className="px-4 py-2 hover:bg-gray-100 cursor-pointer border-b border-gray-100 last:border-b-0"
                            >
                              <div className="font-medium">{ville.communes}</div>
                              <div className="text-sm text-gray-600">{ville.code_postal}</div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Date de naissance</label>
                      <input
                        type="date"
                        value={formData.date_naissance}
                        onChange={(e) => setFormData({...formData, date_naissance: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Numéro de sécurité sociale</label>
                      <input
                        type="text"
                        value={formData.num_securite_social}
                        onChange={(e) => setFormData({...formData, num_securite_social: e.target.value})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Chemin OneDrive
                        <span className="text-xs text-gray-500 ml-1">(Chemin relatif depuis OneDrive)</span>
                      </label>
                      <div className="flex gap-2">
                        <input
                          type="text"
                          value={formData.ondrive_path}
                          onChange={(e) => setFormData({...formData, ondrive_path: e.target.value})}
                          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                          placeholder="Ex: ./OneDrive/Administration/Volet social/0-Dossier salarié/Nom_Prenom"
                        />
                        {formData.ondrive_path && (
                          <button
                            type="button"
                            onClick={async () => {
                              const result = await testOneDrivePath(formData.ondrive_path);
                              if (result.success) {
                                if (result.exists) {
                                  alert(`✅ Chemin valide!\n\nChemin résolu: ${result.resolved_path}\n\nOneDrive trouvé: ${result.onedrive_base}`);
                                } else {
                                  alert(`⚠️ Chemin résolu mais dossier non trouvé\n\nChemin résolu: ${result.resolved_path}\n\nOneDrive trouvé: ${result.onedrive_base}`);
                                }
                              } else {
                                alert(`❌ Erreur: ${result.error}`);
                              }
                            }}
                            className="mt-1 px-3 py-2 bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200 text-sm"
                          >
                            Tester
                          </button>
                        )}
                      </div>
                      <div className="mt-2 text-xs text-gray-600">
                        <div className="font-medium mb-1">Exemples de chemins relatifs :</div>
                        <div className="space-y-1">
                          <div>• ./OneDrive/Administration/Volet social/0-Dossier salarié/Nom_Prenom</div>
                          <div>• ./OneDrive/ATARYS/Salariés/Nom_Prenom</div>
                          <div>• ./OneDrive/Contrats/Nom_Prenom</div>
                          <div>• ./OneDrive/Planning/Nom_Prenom</div>
                        </div>
                        <div className="mt-2 text-green-600">
                          💡 L'application détecte automatiquement OneDrive sur votre poste
                        </div>
                        <div className="mt-1 text-blue-600 text-xs">
                          ⚠️ Le système enlève automatiquement "OneDrive" du chemin pour éviter la duplication
                        </div>
                      </div>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Familles d'ouvrages
                        <span className="text-xs text-gray-500 ml-1">(Ctrl+clic pour sélection multiple)</span>
                      </label>
                      <select
                        multiple
                        size="4"
                        value={formData.famille_ouvrages_ids}
                        onChange={(e) => setFormData({...formData, famille_ouvrages_ids: Array.from(e.target.selectedOptions, option => option.value)})}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      >
                        {familleOuvrages.length > 0 ? (
                          familleOuvrages.map((famille) => (
                            <option key={famille.id} value={famille.id}>
                              {famille.libelle}
                            </option>
                          ))
                        ) : (
                          <option disabled>Aucune famille d'ouvrage disponible</option>
                        )}
                      </select>
                      {formData.famille_ouvrages_ids.length > 0 && (
                        <div className="mt-2 text-xs text-gray-600">
                          Sélectionné(s) : {formData.famille_ouvrages_ids.length} famille(s)
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex justify-end space-x-3 pt-4">
                    <button
                      type="button"
                      onClick={() => setShowModal(false)}
                      className="bg-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-400"
                    >
                      Annuler
                    </button>
                    <button
                      type="submit"
                      className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                    >
                      {editingSalary ? 'Modifier' : 'Créer'}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        )}
    </PageLayout>
  );
};

export default Module9_1; 