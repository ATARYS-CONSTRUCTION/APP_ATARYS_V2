import React from 'react'

function PlanningSalaries() {
  return (
    <div className="p-4">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Module 1.1 - Planning Salariés</h1>
        <div className="atarys-card">
          <p className="text-gray-600">
            Module en cours de développement. Cette page affichera le planning dynamique des salariés 
            avec filtrage par dates d'entrée/sortie.
          </p>
          <div className="mt-4 p-3 bg-blue-50 rounded">
            <p className="text-sm text-blue-800">
              <strong>Fonctionnalités prévues :</strong>
            </p>
            <ul className="text-sm text-blue-700 mt-2 ml-4">
              <li>• Affichage dynamique selon les dates</li>
              <li>• Scroll automatique vers la date du jour</li>
              <li>• Gestion des jours fériés</li>
              <li>• Interface responsive</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PlanningSalaries 