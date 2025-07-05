import React from 'react';

export function PageLayout({ children, title, variant = "default", showSidebar = false }) {
  // Gestion des variantes de largeur
  const getWidthClass = () => {
    switch (variant) {
      case "wide":
        return "max-w-6xl";
      case "ultrawide":
        return "max-w-full";
      case "full":
        return "w-full";
      case "standard":
        return "max-w-5xl";
      default:
        return "max-w-4xl";
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className={`mx-auto px-4 py-6 ${getWidthClass()}`}>
        {title && (
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
          </div>
        )}
        <div className="space-y-6">
          {children}
        </div>
      </div>
    </div>
  );
}

export function Card({ children, padding = "default", className = "", planningMode = false }) {
  const getPaddingClass = () => {
    // Exception pour les composants de planning - préserver le padding existant
    if (planningMode) {
      switch (padding) {
        case "tight":
          return "p-2";
        case "loose":
          return "p-8";
        case "none":
          return "";
        default:
          return "p-6";
      }
    }
    
    // Standards ATARYS pour les autres composants
    switch (padding) {
      case "tight":
        return "p-2";
      case "loose":
        return "p-8";
      case "none":
        return "";
      case "standard":
        return "p-4"; // 16px selon standards ATARYS
      default:
        return "p-4"; // 16px par défaut
    }
  };

  return (
    <div className={`bg-white rounded-lg shadow-lg ${getPaddingClass()} ${className}`}>
      {children}
    </div>
  );
}

export function GridLayout({ children, columns = "1", gap = "standard" }) {
  const getColumnsClass = () => {
    const variants = {
      "1": "grid-cols-1",
      "2": "grid-cols-1 md:grid-cols-2",
      "8-4": "grid-cols-1 lg:grid-cols-12",
      "7-5": "grid-cols-1 lg:grid-cols-12", 
      "6-6": "grid-cols-1 md:grid-cols-2"
    };
    return variants[columns] || "grid-cols-1";
  };
  
  const getGapClass = () => {
    switch (gap) {
      case "tight":
        return "gap-2";
      case "loose":
        return "gap-6";
      case "standard":
        return "gap-3"; // 12px selon standards ATARYS
      default:
        return "gap-3";
    }
  };
  
  // Gestion spéciale pour les variants 8-4 et 7-5
  if (columns === "8-4") {
    return (
      <div className={`grid ${getColumnsClass()} ${getGapClass()}`}>
        <div className="lg:col-span-8">{children[0]}</div>
        <div className="lg:col-span-4">{children[1]}</div>
      </div>
    );
  }
  
  if (columns === "7-5") {
    return (
      <div className={`grid ${getColumnsClass()} ${getGapClass()}`}>
        <div className="lg:col-span-7">{children[0]}</div>
        <div className="lg:col-span-5">{children[1]}</div>
      </div>
    );
  }

  return (
    <div className={`grid ${getColumnsClass()} ${getGapClass()}`}>
      {children}
    </div>
  );
}

// Nouveau composant FormLayout pour les formulaires
export function FormLayout({ children, gap = "standard" }) {
  const getGapClass = () => {
    switch (gap) {
      case "tight":
        return "gap-2";
      case "loose":
        return "gap-6";
      case "standard":
        return "gap-4"; // 16px selon standards ATARYS
      default:
        return "gap-4";
    }
  };
  
  return (
    <div className={`grid grid-cols-1 md:grid-cols-2 ${getGapClass()}`}>
      {children}
    </div>
  );
}

// Nouveau composant FormSection pour structurer les formulaires
export function FormSection({ children, title, divider = false }) {
  return (
    <div className={`${divider ? 'border-t pt-4 mt-4' : ''}`}>
      {title && (
        <h3 className="text-lg font-semibold mb-3 text-gray-900">{title}</h3>
      )}
      {children}
    </div>
  );
}

// Nouveau composant InputGroup pour grouper les inputs
export function InputGroup({ children }) {
  return (
    <div className="space-y-3">
      {children}
    </div>
  );
}

// Composant ActionButtonGroup pour les boutons d'action
export function ActionButtonGroup({ children, variant = "default" }) {
  const getLayoutClass = () => {
    switch (variant) {
      case "inline":
        return "flex gap-3 items-center";
      case "stack":
        return "flex flex-col gap-2";
      case "spread":
        return "flex justify-between items-center";
      default:
        return "flex gap-3";
    }
  };

  return (
    <div className={`${getLayoutClass()} mt-4`}>
      {children}
    </div>
  );
} 