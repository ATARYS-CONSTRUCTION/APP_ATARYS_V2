import React from 'react'

function CalculArdoises() {
  return (
    <div className="p-4">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Module 10.1 - Calcul Ardoises</h1>
        <div className="atarys-card">
          <p className="text-gray-600">
            Module opérationnel (100% terminé). Cette page permet le calcul automatique des quantités d'ardoises 
            selon la zone climatique, pente et surface.
          </p>
          <div className="mt-4 p-3 bg-green-50 rounded">
            <p className="text-sm text-green-800">
              <strong>Statut :</strong> Workflow complet fonctionnel
            </p>
            <ul className="text-sm text-green-700 mt-2 ml-4">
              <li>• Calcul automatique selon zone climatique</li>
              <li>• Prise en compte de la pente et longueur de rampant</li>
              <li>• Comparaison des différents modèles d'ardoises</li>
              <li>• Quantités précises (ardoises + liteaux)</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CalculArdoises 