import React, { useState, useEffect } from 'react';

// Schéma de formulaire pour articles_atarys
const FORM_SCHEMA = {
  "table_name": "articles_atarys",
  "columns": [
    {
      "name": "reference",
      "type": "text",
      "required": true,
      "validation": {
        "maxlength": "100"
      },
      "default": "",
      "label": "Référence"
    },
    {
      "name": "libelle",
      "type": "text",
      "required": true,
      "validation": {},
      "default": "",
      "label": "Libellé"
    },
    {
      "name": "prix_achat",
      "type": "number",
      "required": false,
      "validation": {
        "step": "0.01",
        "min": "0"
      },
      "default": "0.00",
      "label": "Prix d'achat"
    },
    {
      "name": "coefficient",
      "type": "number",
      "required": false,
      "validation": {
        "step": "0.01",
        "min": "0"
      },
      "default": "1.00",
      "label": "Coefficient"
    },
    {
      "name": "prix_unitaire",
      "type": "number",
      "required": false,
      "validation": {
        "step": "0.01",
        "min": "0"
      },
      "default": "0.00",
      "label": "Prix unitaire"
    },
    {
      "name": "unite",
      "type": "text",
      "required": false,
      "validation": {
        "maxlength": "20"
      },
      "default": "NC",
      "label": "Unité"
    },
    {
      "name": "tva_pct",
      "type": "number",
      "required": false,
      "validation": {
        "step": "0.01",
        "min": "0"
      },
      "default": "20.00",
      "label": "TVA (%)"
    },
    {
      "name": "famille",
      "type": "text",
      "required": false,
      "validation": {
        "maxlength": "30"
      },
      "default": "Général",
      "label": "Famille"
    },
    {
      "name": "actif",
      "type": "checkbox",
      "required": false,
      "validation": {},
      "default": true,
      "label": "Actif"
    },
    {
      "name": "date_import",
      "type": "date",
      "required": false,
      "validation": {},
      "default": "",
      "label": "Date d'import"
    },
    {
      "name": "date_maj",
      "type": "date",
      "required": false,
      "validation": {},
      "default": "",
      "label": "Date de mise à jour"
    }
  ]
};

export default function AddRowForm({ onAdd, onCancel }) {
  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState({});

  // Initialiser les valeurs par défaut
  useEffect(() => {
    const defaults = {};
    FORM_SCHEMA.columns.forEach(col => {
      defaults[col.name] = col.default;
    });
    setFormData(defaults);
  }, []);

  const handleChange = (fieldName, value) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: value
    }));
    
    // Effacer l'erreur pour ce champ
    if (errors[fieldName]) {
      setErrors(prev => ({
        ...prev,
        [fieldName]: null
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    FORM_SCHEMA.columns.forEach(col => {
      if (col.required && (!formData[col.name] || formData[col.name].toString().trim() === '')) {
        newErrors[col.name] = `${col.label} est obligatoire`;
      }
    });
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      // Convertir les types de données
      const processedData = { ...formData };
      
      FORM_SCHEMA.columns.forEach(col => {
        if (col.type === 'number') {
          processedData[col.name] = Number(processedData[col.name]) || 0;
        } else if (col.type === 'checkbox') {
          processedData[col.name] = Boolean(processedData[col.name]);
        }
      });
      
      onAdd(processedData);
    }
  };

  const renderField = (col) => {
    const value = formData[col.name] || '';
    const error = errors[col.name];
    
    const commonProps = {
      id: col.name,
      name: col.name,
      value: value,
      onChange: (e) => handleChange(col.name, e.target.value),
      className: `w-full px-3 py-2 border rounded-md ${
        error ? 'border-red-500' : 'border-gray-300'
      } focus:outline-none focus:ring-2 focus:ring-blue-500`,
      ...col.validation
    };

    switch (col.type) {
      case 'checkbox':
        return (
          <input
            type="checkbox"
            checked={Boolean(value)}
            onChange={(e) => handleChange(col.name, e.target.checked)}
            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
        );
      
      case 'date':
        return (
          <input
            type="date"
            {...commonProps}
            value={value || ''}
          />
        );
      
      case 'number':
        return (
          <input
            type="number"
            {...commonProps}
            step={col.validation.step || '1'}
            min={col.validation.min || '0'}
          />
        );
      
      default:
        return (
          <input
            type="text"
            {...commonProps}
          />
        );
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-gray-900">
            ➕ Ajouter un nouvel article
          </h2>
          <button
            onClick={onCancel}
            className="text-gray-400 hover:text-gray-600"
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {FORM_SCHEMA.columns.map(col => (
              <div key={col.name} className="space-y-2">
                <label htmlFor={col.name} className="block text-sm font-medium text-gray-700">
                  {col.label}
                  {col.required && <span className="text-red-500 ml-1">*</span>}
                </label>
                
                <div className="flex items-center space-x-2">
                  {renderField(col)}
                  {col.type === 'checkbox' && (
                    <span className="text-sm text-gray-600">{col.label}</span>
                  )}
                </div>
                
                {errors[col.name] && (
                  <p className="text-sm text-red-600">{errors[col.name]}</p>
                )}
              </div>
            ))}
          </div>

          <div className="flex justify-end space-x-3 pt-4 border-t">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 font-medium"
            >
              Annuler
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium"
            >
              Ajouter l'article
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 