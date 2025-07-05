import React from 'react'

function ListeChantiers() {
  return (
    <div className="p-4">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Module 3.1 - Liste Chantiers</h1>
        <div className="atarys-card">
          <p className="text-gray-600">
            Module en cours de développement (95% terminé). Cette page affichera la liste complète des chantiers 
            avec fonctionnalités d'insertion de devis Excel.
          </p>
          <div className="mt-4 p-3 bg-green-50 rounded">
            <p className="text-sm text-green-800">
              <strong>Statut :</strong> Architecture migrée, fonctionnalités à terminer
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ListeChantiers 