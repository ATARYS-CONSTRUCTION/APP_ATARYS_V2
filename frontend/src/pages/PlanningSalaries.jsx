import React, { useState, useEffect, useRef } from 'react';
import { PageLayout, Card } from '../components/Layout';
import { useMenu } from '../contexts/MenuContext';

// Données des salariés (copiées du fichier JSON de référence)
const SALARIES_DATA = [
  {
    "id": 1,
    "prenom": "ROMAIN",
    "nom": "GOUJON",
    "salaire_brut_horaire": 14.59,
    "nombre_heure_hebdo": 39.0,
    "date_entree": "2018-05-14",
    "date_sortie": "",
    "niveau_id": 5,
    "colonne_planning": 1
  },
  {
    "id": 2,
    "prenom": "VINCENT",
    "nom": "CORMONT",
    "salaire_brut_horaire": 14.59,
    "nombre_heure_hebdo": 35.0,
    "date_entree": "2020-09-14",
    "date_sortie": "",
    "niveau_id": 5,
    "colonne_planning": 2
  },
  {
    "id": 3,
    "prenom": "ITAI",
    "nom": "BENGAL",
    "salaire_brut_horaire": 14.59,
    "nombre_heure_hebdo": 32.0,
    "date_entree": "2017-01-18",
    "date_sortie": "",
    "niveau_id": 5,
    "colonne_planning": 3
  },
  {
    "id": 4,
    "prenom": "REMI",
    "nom": "LINARES",
    "salaire_brut_horaire": 10.69,
    "nombre_heure_hebdo": 35.0,
    "date_entree": "2023-03-01",
    "date_sortie": "2025-07-30",
    "niveau_id": 8,
    "colonne_planning": 4
  },
  {
    "id": 5,
    "prenom": "MERLIN",
    "nom": "RABILLER-LAHAYE",
    "salaire_brut_horaire": 12.16,
    "nombre_heure_hebdo": 35.0,
    "date_entree": "2024-09-01",
    "date_sortie": "2025-08-30",
    "niveau_id": 8,
    "colonne_planning": 5
  },
  {
    "id": 6,
    "prenom": "MARTIN",
    "nom": "ARRIBARD",
    "salaire_brut_horaire": 12.16,
    "nombre_heure_hebdo": 35.0,
    "date_entree": "2024-09-01",
    "date_sortie": "2026-08-31",
    "niveau_id": 9,
    "colonne_planning": 6
  },
  {
    "id": 7,
    "prenom": "DAVID",
    "nom": "BETIN",
    "salaire_brut_horaire": 15.5,
    "nombre_heure_hebdo": 35.0,
    "date_entree": "2025-04-14",
    "date_sortie": "",
    "niveau_id": 6,
    "colonne_planning": 7
  },
  {
    "id": 8,
    "prenom": "YANN",
    "nom": "OILLO",
    "salaire_brut_horaire": 16.8,
    "nombre_heure_hebdo": 39.0,
    "date_entree": "2019-02-01",
    "date_sortie": "",
    "niveau_id": 7,
    "colonne_planning": 8
  },
  {
    "id": 9,
    "prenom": "JULIEN",
    "nom": "LE BADEZET",
    "salaire_brut_horaire": 18.0,
    "nombre_heure_hebdo": 42.0,
    "date_entree": "2015-03-01",
    "date_sortie": "",
    "niveau_id": 7,
    "colonne_planning": 9
  },
  {
    "id": 10,
    "prenom": "PAOLO",
    "nom": "IZQUIERDO",
    "salaire_brut_horaire": 10.69,
    "nombre_heure_hebdo": 35.0,
    "date_entree": "2025-09-01",
    "date_sortie": "2026-08-31",
    "niveau_id": 9,
    "colonne_planning": 5
  }
];

function getWeekNumber(date) {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

function getEasterMonday(year) {
  const a = year % 19;
  const b = Math.floor(year / 100);
  const c = year % 100;
  const d = Math.floor(b / 4);
  const e = b % 4;
  const f = Math.floor((b + 8) / 25);
  const g = Math.floor((b - f + 1) / 3);
  const h = (19 * a + b - d - g + 15) % 30;
  const i = Math.floor(c / 4);
  const k = c % 4;
  const l = (32 + 2 * e + 2 * i - h - k) % 7;
  const m = Math.floor((a + 11 * h + 22 * l) / 451);
  const month = Math.floor((h + l - 7 * m + 114) / 31);
  const day = ((h + l - 7 * m + 114) % 31) + 1;
  const easter = new Date(year, month - 1, day);
  easter.setDate(easter.getDate() + 1);
  return easter;
}

function getAscensionThursday(year) {
  const easterMonday = getEasterMonday(year);
  const ascension = new Date(easterMonday);
  ascension.setDate(easterMonday.getDate() + 38);
  return ascension;
}

function getPentecostMonday(year) {
  const easterMonday = getEasterMonday(year);
  const pentecost = new Date(easterMonday);
  pentecost.setDate(easterMonday.getDate() + 49);
  return pentecost;
}

function isHoliday(date) {
  const year = date.getFullYear();
  const month = date.getMonth();
  const day = date.getDate();
  const fixedHolidays = [
    { month: 0, day: 1 },
    { month: 4, day: 1 },
    { month: 4, day: 8 },
    { month: 6, day: 14 },
    { month: 7, day: 15 },
    { month: 10, day: 1 },
    { month: 10, day: 11 },
    { month: 11, day: 25 }
  ];
  for (const holiday of fixedHolidays) {
    if (month === holiday.month && day === holiday.day) return true;
  }
  const easterMonday = getEasterMonday(year);
  const ascension = getAscensionThursday(year);
  const pentecostMonday = getPentecostMonday(year);
  return date.getTime() === easterMonday.getTime()
      || date.getTime() === ascension.getTime()
      || date.getTime() === pentecostMonday.getTime();
}

function getSalariesForDate(date, salaries) {
  if (!salaries || !Array.isArray(salaries)) return Array(12).fill("");
  
  const result = Array(12).fill("");
  salaries.forEach(s => {
    if (!s || !s.date_entree || !s.colonne_planning) return;
    
    const entree = new Date(s.date_entree);
    const sortie = s.date_sortie ? new Date(s.date_sortie) : null;
    
    if (entree <= date && (!sortie || date <= sortie)) {
      result[s.colonne_planning - 1] = s.prenom;
    }
  });
  return result;
}

const jours = ["dim.", "lun.", "mar.", "mer.", "jeu.", "ven.", "sam."];

function PlanningSalaries() {
  const { menuOpen } = useMenu();
  const planningContainerRef = useRef(null);
  const [isMounted, setIsMounted] = useState(false);
  const [rows, setRows] = useState([]);
  const [dateVisible, setDateVisible] = useState(new Date());
  const [todayRowIndex, setTodayRowIndex] = useState(null);

  // Utiliser les données statiques
  const salaries = SALARIES_DATA;

  useEffect(() => {
    if (!salaries) return;

    const startDate = new Date("2025-01-01");
    const endDate = new Date("2027-01-01");
    const today = new Date();
    const tempRows = [];
    let todayRowIndex = null;

    for (let d = new Date(startDate); d < endDate; d.setDate(d.getDate() + 1)) {
      const isWeekend = d.getDay() === 0 || d.getDay() === 6;
      const isHolidayDay = isHoliday(d);
      const isToday = d.toDateString() === today.toDateString();
      const weekNum = getWeekNumber(new Date(d));
      const showWeek = d.getDay() === 1 ? "S" + weekNum : "";
      const jourLabel = `${jours[d.getDay()]} ${d.toLocaleDateString("fr-FR")}`;
      let bg = "bg-white";
      if (isWeekend || isHolidayDay) bg = "bg-gray-200";
      if (isToday) {
        bg = "bg-blue-200";
        setTodayRowIndex(tempRows.length);
      }
      tempRows.push({
        date: new Date(d),
        bg,
        showWeek,
        jourLabel,
      });
    }

    setRows(tempRows);
  }, [salaries]);

  // Effet pour gérer le défilement vers la date du jour
  useEffect(() => {
    setIsMounted(true);
    return () => setIsMounted(false);
  }, []);

  // Effet pour gérer le défilement vers la date du jour
  useEffect(() => {
    if (!isMounted || todayRowIndex === null || !planningContainerRef.current) return;

    const scrollToToday = () => {
      const rows = planningContainerRef.current.querySelectorAll('tbody tr');
      if (todayRowIndex >= 0 && todayRowIndex < rows.length) {
        // Centrer la date actuelle dans la vue
        rows[todayRowIndex].scrollIntoView({ 
          behavior: 'auto', 
          block: 'center' 
        });
      }
    };

    const timer = setTimeout(scrollToToday, 100);
    return () => clearTimeout(timer);
  }, [isMounted, todayRowIndex]);

  // Effet pour gérer la mise à jour de la date visible au défilement
  useEffect(() => {
    if (!isMounted || !planningContainerRef.current) return;

    const updateVisibleDate = () => {
      const container = planningContainerRef.current;
      const rows = container.querySelectorAll('tbody tr');
      
      // Trouver la première ligne visible au milieu du conteneur
      const containerRect = container.getBoundingClientRect();
      
      for (let row of rows) {
        const rowRect = row.getBoundingClientRect();
        const rowMiddle = rowRect.top + (rowRect.height / 2);
        
        // Vérifier si le milieu de la ligne est dans la zone visible du conteneur
        if (rowMiddle >= containerRect.top && rowMiddle <= containerRect.bottom) {
          const dateStr = row.getAttribute('data-date');
          if (dateStr) {
            setDateVisible(new Date(dateStr));
          } else {
            // Fallback si data-date n'est pas disponible
            const text = row.querySelector('td:nth-child(2)')?.textContent;
            const match = text?.match(/(\d{2})\/(\d{2})\/(\d{4})/);
            if (match) {
              const [_, jour, mois, annee] = match;
              setDateVisible(new Date(`${annee}-${mois}-${jour}`));
            }
          }
          break;
        }
      }
    };

    const container = planningContainerRef.current;
    container.addEventListener('scroll', updateVisibleDate);
    
    // Mettre à jour la date visible après le rendu initial
    const timer = setTimeout(updateVisibleDate, 100);
    
    return () => {
      container.removeEventListener('scroll', updateVisibleDate);
      clearTimeout(timer);
    };
  }, [isMounted, rows]);

  // Nombre de colonnes de salariés selon l'état du menu
  const maxSalariesColumns = menuOpen ? 7 : 11;
  
  // Fonction pour obtenir les salariés avec limitation de colonnes
  const getSalariesForDateLimited = (date, salaries) => {
    const allSalaries = getSalariesForDate(date, salaries);
    const limited = allSalaries.slice(0, maxSalariesColumns);
    return limited;
  };

  return (
    <PageLayout variant="ultrawide" title="Planning ATARYS">
      <Card padding="none" className="pb-4" planningMode={true}>
        <div 
          ref={planningContainerRef}
          className="overflow-y-auto border border-gray-300 rounded bg-white shadow-lg" 
          style={{ maxHeight: "calc(100vh - 120px)" }}
        >
          <table className="table-auto w-full text-base">
            <thead className="sticky top-0 z-10 bg-white">
              <tr>
                <th className="px-1 py-1.5 min-w-16 border bg-gray-200 text-center font-semibold text-xs">Semaine</th>
                <th className="px-2 py-1.5 min-w-6 border bg-gray-200 font-semibold text-xs">Date</th>
                {getSalariesForDateLimited(dateVisible, salaries).map((prenom, i) => (
                  <th key={i} className="px-1 py-1.5 min-w-24 border bg-gray-200 text-center font-semibold text-xs">{prenom}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, i) => (
                <tr 
                  key={i} 
                  className={`${row.bg} hover:bg-opacity-75 transition-colors`}
                  data-date={row.date.toISOString()}
                >
                  <td className="px-1 py-1.5 border text-center font-semibold text-xs">{row.showWeek}</td>
                  <td className="px-2 py-1.5 border font-medium text-xs">{row.jourLabel}</td>
                  {getSalariesForDateLimited(row.date, salaries).map((_, j) => (
                    <td key={j} className="px-1 py-1.5 border min-h-7"></td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </PageLayout>
  );
}

export default PlanningSalaries; 