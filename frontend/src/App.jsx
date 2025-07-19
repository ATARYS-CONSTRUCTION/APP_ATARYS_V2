import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { MenuProvider } from './contexts/MenuContext'
import Menu from './components/Menu'
import Home from './pages/Home'

// Import des pages selon nomenclature ATARYS
import PlanningSalaries from './pages/PlanningSalaries'
import PlanningChantiers from './pages/PlanningChantiers'
import ListeChantiers from './pages/ListeChantiers'
import ChantiersProjets from './pages/ChantiersProjets'
import ChantiersSignes from './pages/ChantiersSignes'
import ChantiersEnCours from './pages/ChantiersEnCours'
import ChantiersArchives from './pages/ChantiersArchives'
import CalculArdoises from './pages/CalculArdoises'
import BaseDeDonnees from './pages/BaseDeDonnees'
import Module9_1 from './pages/Module9_1'
import Module9_2 from './pages/Module9_2'
import Module9_3 from './pages/Module9_3'

function App() {
  return (
    <MenuProvider>
      <Router>
        <div className="flex h-screen bg-gray-50">
          <Menu />
          <div className="flex-1 overflow-auto">
            <Routes>
              <Route path="/" element={<Home />} />
              
              {/* Module 1 - Planning */}
              <Route path="/planning-salaries" element={<PlanningSalaries />} />
              <Route path="/planning-chantiers" element={<PlanningChantiers />} />
              
              {/* Module 3 - Chantiers */}
              <Route path="/liste-chantiers" element={<ListeChantiers />} />
              <Route path="/chantiers-projets" element={<ChantiersProjets />} />
              <Route path="/chantiers-signes" element={<ChantiersSignes />} />
              <Route path="/chantiers-en-cours" element={<ChantiersEnCours />} />
              <Route path="/chantiers-archives" element={<ChantiersArchives />} />
              
              {/* Module 9 - Social */}
              <Route path="/module-9-1" element={<Module9_1 />} />
              <Route path="/module-9-2" element={<Module9_2 />} />
              <Route path="/module-9-3" element={<Module9_3 />} />
              
              {/* Module 10 - Outils */}
              <Route path="/calcul-ardoises" element={<CalculArdoises />} />
              {/* Module 12 - Paramètres */}
              <Route path="/base-donnees" element={<BaseDeDonnees />} />
            </Routes>
          </div>
        </div>
      </Router>
    </MenuProvider>
  )
}

export default App 