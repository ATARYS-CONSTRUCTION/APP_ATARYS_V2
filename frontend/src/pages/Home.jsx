import React from 'react'

function Home() {
  return (
    <div className="p-4">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">ATARYS - Gestion Charpente</h1>
          <p className="text-gray-600">Application de gestion d'entreprise - Charpente, Couverture, Menuiserie</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Module 1 - Planning */}
          <div className="atarys-card">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Module 1 - Planning</h3>
            <div className="space-y-2">
              <a href="/planning-salaries" className="block text-primary-600 hover:text-primary-700">
                1.1 Planning Salariés
              </a>
              <a href="/planning-chantiers" className="block text-primary-600 hover:text-primary-700">
                1.2 Planning Chantiers
              </a>
            </div>
          </div>

          {/* Module 3 - Chantiers */}
          <div className="atarys-card">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Module 3 - Chantiers</h3>
            <div className="space-y-2">
              <a href="/liste-chantiers" className="block text-primary-600 hover:text-primary-700">
                3.1 Liste Chantiers
              </a>
              <a href="/chantiers-projets" className="block text-primary-600 hover:text-primary-700">
                3.2 Chantiers Projets
              </a>
              <a href="/chantiers-signes" className="block text-primary-600 hover:text-primary-700">
                3.3 Chantiers Signés
              </a>
              <a href="/chantiers-en-cours" className="block text-primary-600 hover:text-primary-700">
                3.4 Chantiers En Cours
              </a>
              <a href="/chantiers-archives" className="block text-primary-600 hover:text-primary-700">
                3.5 Chantiers Archives
              </a>
            </div>
          </div>

          {/* Module 10 - Outils */}
          <div className="atarys-card">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Module 10 - Outils</h3>
            <div className="space-y-2">
              <a href="/calcul-ardoises" className="block text-primary-600 hover:text-primary-700">
                10.1 Calcul Ardoises
              </a>
              <span className="block text-gray-400">10.2 Calcul Structures</span>
              <span className="block text-gray-400">10.3 Calcul Métrés</span>
            </div>
          </div>

          {/* Autres modules (à venir) */}
          <div className="atarys-card">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Autres Modules</h3>
            <div className="space-y-2 text-gray-400">
              <span className="block">Module 2 - Liste des Tâches</span>
              <span className="block">Module 4 - Suivi Chantiers</span>
              <span className="block">Module 5 - Devis-Facturation</span>
              <span className="block">Module 6 - Atelier</span>
              <span className="block">Module 7 - Gestion</span>
              <span className="block">Module 8 - Comptabilité</span>
              <span className="block">Module 9 - Social</span>
            </div>
          </div>
        </div>

        <div className="mt-8 p-4 bg-blue-50 rounded-lg">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">État du Projet</h3>
          <p className="text-blue-800 mb-2">
            <strong>Objectif :</strong> Remplacer tous les fichiers Excel par une application web complète
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <p className="font-medium text-blue-900">✅ Modules Opérationnels :</p>
              <ul className="text-blue-700 ml-4">
                <li>• Module 9.1 - Liste Salariés</li>
                <li>• Module 10.1 - Calcul Ardoises</li>
                <li>• Architecture Backend complète</li>
              </ul>
            </div>
            <div>
              <p className="font-medium text-blue-900">🔄 En Cours :</p>
              <ul className="text-blue-700 ml-4">
                <li>• Module 3.1 - Liste Chantiers (95%)</li>
                <li>• Module 1.1/1.2 - Planning (90%)</li>
                <li>• Module 5.3 - Devis MEXT (90%)</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home 