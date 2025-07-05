import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useMenu } from '../contexts/MenuContext';

function Menu() {
  const { menuOpen, setMenuOpen } = useMenu();
  const [planningOpen, setPlanningOpen] = useState(false);
  const [listeChantiersOpen, setListeChantiersOpen] = useState(false);
  const [chantiersOpen, setChantiersOpen] = useState(false);
  const [outilsOpen, setOutilsOpen] = useState(false);

  return (
    <aside
      className={`bg-white shadow flex-shrink-0 h-full overflow-y-auto px-2 py-4 transition-all duration-300 ${menuOpen ? 'w-64' : 'w-16'}`}
    >
      <div className="flex justify-end mb-6">
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="text-gray-500 hover:text-black text-lg focus:outline-none"
        >
          {menuOpen ? '⮜' : '⮞'}
        </button>
      </div>
      {menuOpen && (
        <>
          <Link
            to="/"
            className="text-xl font-bold text-black mb-6 block hover:text-blue-600 transition-colors duration-200"
          >
            ATARYS
          </Link>
          <nav className="space-y-3 text-gray-700 font-medium">
            <div>
              <div
                onClick={() => setPlanningOpen(!planningOpen)}
                className="px-2 py-1 rounded hover:bg-gray-200 hover:text-black cursor-pointer flex justify-between items-center"
              >
                <span>PLANNING</span>
                <span className={`text-black transition-transform duration-200 ${planningOpen ? '' : '-rotate-90'}`}>
                  ▼
                </span>
              </div>
              {planningOpen && (
                <div className="ml-4 mt-1 space-y-1 text-sm text-gray-600">
                  <Link className="block hover:text-black" to="/planning-salaries">Planning Salariés</Link>
                  <Link className="block hover:text-black" to="/planning-chantiers">Planning Chantiers</Link>
                </div>
              )}
            </div>
            <Link className="block px-2 py-1 rounded hover:bg-gray-200 hover:text-black" to="#">LISTE DES TACHES</Link>
            <div>
              <div
                onClick={() => setListeChantiersOpen(!listeChantiersOpen)}
                className="px-2 py-1 rounded hover:bg-gray-200 hover:text-black cursor-pointer flex justify-between items-center"
              >
                <span>LISTE CHANTIERS</span>
                <span className={`text-black transition-transform duration-200 ${listeChantiersOpen ? '' : '-rotate-90'}`}>
                  ▼
                </span>
              </div>
              {listeChantiersOpen && (
                <div className="ml-4 mt-1 space-y-1 text-sm text-gray-600">
                  <Link className="block hover:text-black" to="/liste-chantiers">Liste Chantiers</Link>
                  <Link className="block hover:text-black" to="/chantiers-projets">Chantiers Projets</Link>
                  <Link className="block hover:text-black" to="/chantiers-signes">Chantiers Signés</Link>
                  <Link className="block hover:text-black" to="/chantiers-en-cours">Chantiers En Cours</Link>
                  <Link className="block hover:text-black" to="/chantiers-archives">Chantiers Archives</Link>
                </div>
              )}
            </div>
            <div>
              <div
                onClick={() => setChantiersOpen(!chantiersOpen)}
                className="px-2 py-1 rounded hover:bg-gray-200 hover:text-black cursor-pointer flex justify-between items-center"
              >
                <span>CHANTIERS</span>
                <span className={`text-black transition-transform duration-200 ${chantiersOpen ? '' : '-rotate-90'}`}>
                  ▼
                </span>
              </div>
              {chantiersOpen && (
                <div className="ml-4 mt-1 space-y-1 text-sm text-gray-600">
                  <Link className="block hover:text-black" to="/suivi-chantier">Suivi de Chantier</Link>
                  <Link className="block hover:text-black" to="/notes-chantier">Notes de Chantier</Link>
                  <Link className="block hover:text-black" to="/commandes">Commandes</Link>
                  <Link className="block hover:text-black" to="/documents">Documents</Link>
                </div>
              )}
            </div>
            <Link className="block px-2 py-1 rounded hover:bg-gray-200 hover:text-black" to="#">DEVIS-FACTURATION</Link>
            <Link className="block px-2 py-1 rounded hover:bg-gray-200 hover:text-black" to="#">ATELIER</Link>
            <Link className="block px-2 py-1 rounded hover:bg-gray-200 hover:text-black" to="#">GESTION</Link>
            <Link className="block px-2 py-1 rounded hover:bg-gray-200 hover:text-black" to="#">COMPTABILITE</Link>
            <Link className="block px-2 py-1 rounded hover:bg-gray-200 hover:text-black" to="#">SOCIAL</Link>
            <div>
              <div
                onClick={() => setOutilsOpen(!outilsOpen)}
                className="px-2 py-1 rounded hover:bg-gray-200 hover:text-black cursor-pointer flex justify-between items-center"
              >
                <span>OUTILS</span>
                <span className={`text-black transition-transform duration-200 ${outilsOpen ? '' : '-rotate-90'}`}>
                  ▼
                </span>
              </div>
              {outilsOpen && (
                <div className="ml-4 mt-1 space-y-1 text-sm text-gray-600">
                  <Link className="block hover:text-black" to="/calcul-ardoises">Calcul ardoises</Link>
                  <Link className="block hover:text-black" to="#">Calcul structures</Link>
                  <Link className="block hover:text-black" to="#">Calcul métrés</Link>
                  <Link className="block hover:text-black" to="#">Occupation du domaine</Link>
                </div>
              )}
            </div>
            <Link className="block px-2 py-1 rounded hover:bg-gray-200 hover:text-black" to="#">ARCHIVES</Link>
            <Link className="block px-2 py-1 rounded hover:bg-gray-200 hover:text-black" to="#">PARAMETRES</Link>
            <Link className="block px-2 py-1 rounded hover:bg-gray-200 hover:text-black" to="#">AIDE</Link>
          </nav>
        </>
      )}
    </aside>
  );
}

export default Menu; 