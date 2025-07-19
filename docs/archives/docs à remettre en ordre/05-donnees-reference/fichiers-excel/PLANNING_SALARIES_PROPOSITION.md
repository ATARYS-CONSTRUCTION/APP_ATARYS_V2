# PROPOSITION - FEUILLE EXCEL PLANNING SALARIÉ ATARYS

> **Basé sur l'analyse de "Planning Atarys 2025 3.xlsm" et "Planning_chantier_excel.txt"**  
> **Objectif : Répondre à "Comment est rempli théoriquement le planning selon l'effectif"**

---

## 🎯 **OBJECTIF PRINCIPAL**

Créer une feuille Excel qui permette d'**insérer rapidement des chantiers selon le nombre d'heures** et de **visualiser la charge théorique de l'effectif**.

---

## 📊 **STRUCTURE PROPOSÉE - 3 ONGLETS**

### **1. ONGLET "PLANNING_SALARIES" - Planning principal**

#### **En-têtes (Ligne 1-3)**
```
A1: [vide]     B1: Date     C1: ROMAIN     D1: VINCENT     E1: ITAI     F1: MERLIN     G1: MARTIN     H1: DAVID     I1: YANN     J1: JULIEN
A2: [vide]     B2: [vide]   C2: 39h/sem    D2: 35h/sem     E2: 32h/sem  F2: 35h/sem    G2: 35h/sem    H2: 35h/sem    I2: 39h/sem    J2: 42h/sem
A3: Semaine    B3: [vide]   C3: 7.5h/j     D3: 7.5h/j      E3: 6.4h/j   F3: 7.5h/j     G3: 7.5h/j     H3: 7.5h/j     I3: 7.5h/j     J3: 8.4h/j
```

#### **Colonnes de données (A4:J367)**
- **Colonne A** : Numéro de semaine (S1, S2, etc.)
- **Colonne B** : Date (format français)
- **Colonnes C-J** : Chantiers affectés aux salariés

#### **Formules de calcul automatique**
```excel
# Calcul jours nécessaires (colonne K)
K4: =SI(C4<>"";ARRONDI.SUP(RECHERCHEV(C4;Liste_Chantiers!$A:$G;7;FAUX)/0.75/7.5;0);"")

# Charge hebdomadaire par salarié (ligne 1)
C1: =SOMMEPROD((C4:C367<>"")*1)&" j"
D1: =SOMMEPROD((D4:D367<>"")*1)&" j"

# Heures planifiées vs théoriques (ligne 2)
C2: =SI(SOMMEPROD((C4:C367<>"")*1)*7.5>39;"Surchargé";"OK")
```

### **2. ONGLET "EFFECTIF_THEORIQUE" - Calculs de charge**

#### **Tableau de synthèse (A1:F20)**
```
A1: SALARIÉ          B1: HEURES/SEM    C1: JOURS/SEM    D1: JOURS PLANIFIÉS    E1: CHARGE %    F1: STATUT
A2: ROMAIN           B2: 39            C2: 5.2          D2: =RECHERCHEV(A2;Planning_Salaries!$C$1:$C$1;1;FAUX)    E2: =D2/C2*100    F2: =SI(E2>100;"SURCHARGÉ";"OK")
A3: VINCENT          B3: 35            C3: 4.7          D3: [formule]           E3: [formule]   F3: [formule]
```

#### **Graphiques de charge**
- **Graphique 1** : Charge hebdomadaire par salarié (%)
- **Graphique 2** : Évolution de la charge sur 12 mois
- **Graphique 3** : Disponibilité par semaine

### **3. ONGLET "INSERTION_RAPIDE" - Interface d'insertion**

#### **Formulaire d'insertion (A1:F10)**
```
A1: INSERTION RAPIDE CHANTIER
A2: Chantier:        B2: [Liste déroulante depuis Liste_Chantiers]
A3: Heures totales:  B3: =SI(B2<>"";RECHERCHEV(B2;Liste_Chantiers!$A:$G;7;FAUX);"")
A4: Jours nécessaires: B4: =ARRONDI.SUP(B3/0.75/7.5;0)
A5: Salarié:         B5: [Liste déroulante des salariés disponibles]
A6: Date de début:   B6: [Sélecteur de date]
A7: [Bouton "Insérer"]
```

#### **Tableau de disponibilité (A12:F20)**
```
A12: SALARIÉ         B12: PROCHAINE DISPONIBILITÉ    C12: JOURS LIBRES    D12: CHARGE ACTUELLE    E12: RECOMMANDATION
A13: ROMAIN          B13: [formule]                  C13: [formule]       D13: [formule]          E13: [formule]
```

---

## 🔧 **FORMULES CLÉS**

### **Calcul automatique des jours**
```excel
# Conversion heures → jours (avec coefficient 0.75)
=ARRONDI.SUP(heures_total/0.75/7.5;0)

# Exemple : 100h vendues = 133h réelles = 18 jours
=ARRONDI.SUP(100/0.75/7.5;0) = 18
```

### **Détection de conflits**
```excel
# Conflit si même chantier sur plusieurs jours consécutifs
=SI(ET(C4<>"";C4=C3);"⚠️";"")

# Conflit si surcharge salarié
=SI(SOMMEPROD((C4:C367<>"")*1)*7.5>39;"SURCHARGÉ";"OK")
```

### **Calcul de disponibilité**
```excel
# Prochaine disponibilité
=SI(SOMMEPROD((C4:C367<>"")*1)=0;"Immédiate";INDEX(B4:B367;EQUIV("";C4:C367;0)+1))

# Jours libres restants
=52-SOMMEPROD((C4:C367<>"")*1)
```

---

## 🎨 **MISE EN FORME CONDITIONNELLE**

### **Règles de couleur**
- **Vert** : Charge normale (≤100%)
- **Orange** : Charge élevée (100-120%)
- **Rouge** : Surcharge (>120%)
- **Gris** : Week-ends et jours fériés
- **Bleu** : Date actuelle

### **Indicateurs visuels**
- **⚠️** : Conflit détecté
- **📅** : Jours fériés
- **🏠** : Week-ends
- **📊** : Charge >100%

---

## 📋 **MACROS VBA PROPOSÉES**

### **Macro "InsérerChantierRapide"**
```vba
Sub InsérerChantierRapide()
    Dim chantier As String
    Dim salarie As String
    Dim dateDebut As Date
    Dim heures As Double
    Dim jours As Integer
    
    ' Récupération des valeurs du formulaire
    chantier = Range("B2").Value
    salarie = Range("B5").Value
    dateDebut = Range("B6").Value
    heures = Range("B3").Value
    
    ' Calcul des jours
    jours = Application.WorksheetFunction.RoundUp(heures / 0.75 / 7.5, 0)
    
    ' Insertion automatique
    Dim colonne As Integer
    colonne = Application.WorksheetFunction.Match(salarie, Range("C1:J1"), 0) + 2
    
    Dim ligneDebut As Integer
    ligneDebut = Application.WorksheetFunction.Match(dateDebut, Range("B:B"), 0)
    
    ' Remplissage des cellules
    Dim i As Integer
    For i = 0 To jours - 1
        Cells(ligneDebut + i, colonne).Value = chantier
    Next i
    
    MsgBox "Chantier " & chantier & " inséré sur " & jours & " jours"
End Sub
```

### **Macro "CalculerChargeTheorique"**
```vba
Sub CalculerChargeTheorique()
    ' Calcul automatique de la charge théorique
    ' Mise à jour des graphiques
    ' Génération du rapport de charge
End Sub
```

---

## 📊 **INDICATEURS DE PERFORMANCE**

### **KPIs automatiques**
- **Taux de charge moyen** : Moyenne des charges par salarié
- **Surcharge détectée** : Nombre de salariés >100%
- **Disponibilité globale** : Jours libres totaux
- **Efficacité planning** : Ratio heures planifiées/heures vendues

### **Alertes automatiques**
- **Surcharge salarié** : Si >120% de charge
- **Conflit planning** : Si même chantier sur périodes chevauchantes
- **Disponibilité faible** : Si <5 jours libres par salarié

---

## 🔄 **WORKFLOW D'UTILISATION**

### **1. Insertion rapide**
1. Sélectionner chantier dans liste déroulante
2. Vérifier heures calculées automatiquement
3. Choisir salarié recommandé
4. Cliquer "Insérer" → Remplissage automatique

### **2. Vérification charge**
1. Consulter onglet "EFFECTIF_THEORIQUE"
2. Vérifier graphiques de charge
3. Ajuster si nécessaire

### **3. Optimisation**
1. Détecter surcharges (rouge)
2. Répartir charge équitablement
3. Valider planning final

---

## ✅ **AVANTAGES DE CETTE PROPOSITION**

### **Simplicité d'utilisation**
- **Insertion en 3 clics** : Chantier → Salarié → Insérer
- **Calculs automatiques** : Heures → Jours → Charge
- **Recommandations** : Salarié optimal suggéré

### **Précision des calculs**
- **Coefficient 0.75** : Prise en compte du temps réel
- **Heures par jour** : Différenciées par salarié
- **Détection conflits** : Automatique

### **Vision globale**
- **Charge théorique** : Par salarié et global
- **Graphiques** : Visualisation immédiate
- **Alertes** : Prévention des surcharges

---

## 🎯 **RÉPONSE À LA QUESTION INITIALE**

**"Comment est rempli théoriquement le planning selon l'effectif ?"**

### **Réponse :**
1. **Calcul automatique** : Heures vendues → Jours nécessaires (×0.75)
2. **Répartition équitable** : Selon disponibilité et charge actuelle
3. **Optimisation continue** : Détection et correction des surcharges
4. **Validation finale** : Respect des contraintes salariés

### **Exemple concret :**
- **Chantier** : 100h vendues
- **Calcul** : 100h ÷ 0.75 ÷ 7.5h/j = 18 jours
- **Répartition** : Salarié disponible avec charge <100%
- **Résultat** : Planning optimisé et équilibré

---

**Cette proposition permet une gestion efficace du planning salarié avec insertion rapide et optimisation automatique de la charge de travail.** 