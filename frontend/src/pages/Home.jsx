import React from 'react';
import { PageLayout, Card, GridLayout } from '../components/Layout';

function Home() {
  // Données des 13 modules ATARYS selon nomenclature officielle
  const modulesATARYS = [
    {
      id: 1,
      title: "PLANNING",
      emoji: "📅",
      color: "bg-blue-50 border-blue-200",
      headerColor: "text-blue-900",
      linkColor: "text-blue-600 hover:text-blue-700",
      status: "operational",
      submodules: [
        { id: "1.1", name: "Planning Salariés", route: "/planning-salaries", active: true },
        { id: "1.2", name: "Planning Chantier", route: "/planning-chantiers", active: true }
      ]
    },
    {
      id: 2,
      title: "LISTE DES TÂCHES",
      emoji: "📋",
      color: "bg-green-50 border-green-200",
      headerColor: "text-green-900",
      linkColor: "text-green-600 hover:text-green-700",
      status: "development",
      submodules: [
        { id: "2.1", name: "Yann", route: "/taches-yann", active: false },
        { id: "2.2", name: "Julien", route: "/taches-julien", active: false }
      ]
    },
    {
      id: 3,
      title: "LISTE CHANTIERS",
      emoji: "🏗️",
      color: "bg-orange-50 border-orange-200",
      headerColor: "text-orange-900",
      linkColor: "text-orange-600 hover:text-orange-700",
      status: "operational",
      submodules: [
        { id: "3.1", name: "Liste Chantiers", route: "/liste-chantiers", active: true },
        { id: "3.2", name: "Chantiers Projets", route: "/chantiers-projets", active: true },
        { id: "3.3", name: "Chantiers Signés", route: "/chantiers-signes", active: true },
        { id: "3.4", name: "Chantiers En Cours", route: "/chantiers-en-cours", active: true },
        { id: "3.5", name: "Chantiers Archives", route: "/chantiers-archives", active: true }
      ]
    },
    {
      id: 4,
      title: "CHANTIERS",
      emoji: "🏠",
      color: "bg-purple-50 border-purple-200",
      headerColor: "text-purple-900",
      linkColor: "text-purple-600 hover:text-purple-700",
      status: "planned",
      submodules: [
        { id: "4.1", name: "Suivi de Chantier", route: "/suivi-chantier", active: false },
        { id: "4.2", name: "Notes de Chantier", route: "/notes-chantier", active: false },
        { id: "4.3", name: "Commandes", route: "/commandes", active: false },
        { id: "4.4", name: "Documents", route: "/documents", active: false }
      ]
    },
    {
      id: 5,
      title: "DEVIS-FACTURATION",
      emoji: "📄",
      color: "bg-indigo-50 border-indigo-200",
      headerColor: "text-indigo-900",
      linkColor: "text-indigo-600 hover:text-indigo-700",
      status: "development",
      submodules: [
        { id: "5.1", name: "Ouvrages et articles BATAPPLI", route: "/batappli", active: false },
        { id: "5.2", name: "Fiche Mètres", route: "/fiche-metres", active: false },
        { id: "5.3", name: "Devis MEXT", route: "/devis-mext", active: false },
        { id: "5.4", name: "Devis Type", route: "/devis-type", active: false }
      ]
    },
    {
      id: 6,
      title: "ATELIER",
      emoji: "🔧",
      color: "bg-red-50 border-red-200",
      headerColor: "text-red-900",
      linkColor: "text-red-600 hover:text-red-700",
      status: "planned",
      submodules: [
        { id: "6.1", name: "Quincaillerie", route: "/quincaillerie", active: false },
        { id: "6.2", name: "Consommables", route: "/consommables", active: false },
        { id: "6.3", name: "Camions", route: "/camions", active: false },
        { id: "6.4", name: "Matériel", route: "/materiel", active: false },
        { id: "6.5", name: "Échafaudage", route: "/echafaudage", active: false }
      ]
    },
    {
      id: 7,
      title: "GESTION",
      emoji: "📊",
      color: "bg-teal-50 border-teal-200",
      headerColor: "text-teal-900",
      linkColor: "text-teal-600 hover:text-teal-700",
      status: "planned",
      submodules: [
        { id: "7.1", name: "Prévisionnel", route: "/previsionnel", active: false },
        { id: "7.2", name: "Synthèse Prévisionnelle", route: "/synthese-previsionnelle", active: false },
        { id: "7.3", name: "Bilans", route: "/bilans", active: false }
      ]
    },
    {
      id: 8,
      title: "COMPTABILITÉ",
      emoji: "💰",
      color: "bg-yellow-50 border-yellow-200",
      headerColor: "text-yellow-900",
      linkColor: "text-yellow-600 hover:text-yellow-700",
      status: "planned",
      submodules: [
        { id: "8.1", name: "TVA", route: "/tva", active: false },
        { id: "8.2", name: "Tableau de Bord", route: "/tableau-bord", active: false }
      ]
    },
    {
      id: 9,
      title: "SOCIAL",
      emoji: "👥",
      color: "bg-pink-50 border-pink-200",
      headerColor: "text-pink-900",
      linkColor: "text-pink-600 hover:text-pink-700",
      status: "operational",
      submodules: [
        { id: "9.1", name: "Liste_salaries", route: "/liste-salaries", active: true },
        { id: "9.2", name: "Fiche mensuelle", route: "/fiche-mensuelle", active: false },
        { id: "9.3", name: "Récap et calculs", route: "/recap-calculs", active: false }
      ]
    },
    {
      id: 10,
      title: "OUTILS",
      emoji: "🛠️",
      color: "bg-gray-50 border-gray-200",
      headerColor: "text-gray-900",
      linkColor: "text-gray-600 hover:text-gray-700",
      status: "operational",
      submodules: [
        { id: "10.1", name: "Calcul_Ardoises", route: "/calcul-ardoises", active: true },
        { id: "10.2", name: "Calcul_structures", route: "/calcul-structures", active: false },
        { id: "10.3", name: "Staravina", route: "/staravina", active: false },
        { id: "10.4", name: "Documents types", route: "/documents-types", active: false }
      ]
    },
    {
      id: 11,
      title: "ARCHIVES",
      emoji: "📁",
      color: "bg-slate-50 border-slate-200",
      headerColor: "text-slate-900",
      linkColor: "text-slate-600 hover:text-slate-700",
      status: "planned",
      submodules: [
        { id: "11.1", name: "Archivage automatique", route: "/archivage", active: false }
      ]
    },
    {
      id: 12,
      title: "PARAMÈTRES",
      emoji: "⚙️",
      color: "bg-stone-50 border-stone-200",
      headerColor: "text-stone-900",
      linkColor: "text-stone-600 hover:text-stone-700",
      status: "operational",
      submodules: [
        { id: "12.1", name: "Base de Données", route: "/base-donnees", active: true }
      ]
    },
    {
      id: 13,
      title: "AIDE",
      emoji: "❓",
      color: "bg-cyan-50 border-cyan-200",
      headerColor: "text-cyan-900",
      linkColor: "text-cyan-600 hover:text-cyan-700",
      status: "planned",
      submodules: [
        { id: "13.1", name: "Documentation", route: "/documentation", active: false }
      ]
    }
  ];

  const getStatusBadge = (status) => {
    switch (status) {
      case 'operational':
        return <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">✅ Opérationnel</span>;
      case 'development':
        return <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">🔄 En cours</span>;
      case 'planned':
        return <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600">📋 Planifié</span>;
      default:
        return null;
    }
  };

  return (
    <PageLayout variant="ultrawide" title="ATARYS - Gestion Charpente">
      <Card padding="standard">
        <div className="mb-6">
          <p className="text-lg text-gray-600 mb-4">
            Application de gestion d'entreprise - Charpente, Couverture, Menuiserie
          </p>
          <div className="flex gap-4 text-sm">
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 bg-green-500 rounded-full"></span>
              <span>Opérationnel</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 bg-yellow-500 rounded-full"></span>
              <span>En développement</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 bg-gray-400 rounded-full"></span>
              <span>Planifié</span>
            </div>
          </div>
        </div>
      </Card>

      <GridLayout columns="1" gap="standard">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {modulesATARYS.map((module) => (
            <Card key={module.id} padding="standard" className={`${module.color} border-2 hover:shadow-lg transition-shadow`}>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">{module.emoji}</span>
                  <h3 className={`text-lg font-semibold ${module.headerColor}`}>
                    {module.id}. {module.title}
                  </h3>
                </div>
                {getStatusBadge(module.status)}
              </div>
              
              <div className="space-y-2">
                {module.submodules.map((submodule) => (
                  <div key={submodule.id} className="flex items-center">
                    {submodule.active ? (
                      <a 
                        href={submodule.route} 
                        className={`block ${module.linkColor} hover:underline font-medium`}
                      >
                        {submodule.id} {submodule.name}
                      </a>
                    ) : (
                      <span className="block text-gray-400">
                        {submodule.id} {submodule.name}
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </Card>
          ))}
        </div>
      </GridLayout>

      <Card padding="standard" className="bg-blue-50 border-2 border-blue-200">
        <h3 className="text-xl font-semibold text-blue-900 mb-4">📈 État du Projet ATARYS V2</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h4 className="font-semibold text-blue-900 mb-2">✅ Modules Opérationnels</h4>
            <ul className="text-blue-700 space-y-1">
              <li>• Module 1.1/1.2 - Planning</li>
              <li>• Module 3.1-3.5 - Liste Chantiers</li>
              <li>• Module 9.1 - Liste Salariés</li>
              <li>• Module 10.1 - Calcul Ardoises</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-blue-900 mb-2">🔄 En Développement</h4>
            <ul className="text-blue-700 space-y-1">
              <li>• Module 2.1/2.2 - Liste des Tâches</li>
              <li>• Module 5.1-5.4 - Devis-Facturation</li>
              <li>• Backend Flask (APIs REST)</li>
              <li>• Base de données SQLite V2</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-blue-900 mb-2">🎯 Objectif Phase 1</h4>
            <ul className="text-blue-700 space-y-1">
              <li>• Remplacer 17 onglets Excel</li>
              <li>• 7 modules critiques terminés</li>
              <li>• Application web complète</li>
              <li>• Deadline : Mi-octobre 2025</li>
            </ul>
          </div>
        </div>
      </Card>
      <div className="mt-6">
        <a href="/base-donnees" className="inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 font-semibold">
          Base de Données
        </a>
      </div>
    </PageLayout>
  );
}

export default Home; 