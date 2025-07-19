import React from 'react';
import { PageLayout, GridLayout } from '../components/Layout';

const Module9_2 = () => {
  return (
    <PageLayout title="FICHE MENSUELLE">
      <GridLayout>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Fiche mensuelle des salariés</h2>
          <p className="text-gray-600">
            Module en cours de développement selon les standards ATARYS V2.
          </p>
          <div className="mt-4 p-4 bg-blue-50 rounded-lg">
            <h3 className="font-medium text-blue-800 mb-2">Fonctionnalités prévues :</h3>
            <ul className="text-blue-700 space-y-1">
              <li>• Génération des fiches mensuelles par salarié</li>
              <li>• Calcul automatique des heures travaillées</li>
              <li>• Gestion des congés et absences</li>
              <li>• Export PDF des fiches</li>
              <li>• Historique des fiches mensuelles</li>
            </ul>
          </div>
        </div>
      </GridLayout>
    </PageLayout>
  );
};

export default Module9_2; 