import { useState } from 'react';

export default function IngredientList({ ingredients, setIngredients, onGenerate, isGenerating }) {
  const [newItem, setNewItem] = useState('');

  function addItem(e) {
    e.preventDefault();
    const trimmed = newItem.trim();
    if (trimmed && !ingredients.includes(trimmed)) {
      setIngredients([...ingredients, trimmed]);
    }
    setNewItem('');
  }

  function removeItem(name) {
    setIngredients(ingredients.filter((i) => i !== name));
  }

  if (ingredients.length === 0) return null;

  return (
    <div className="w-full bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">
        Detected Ingredients
      </h2>

      <div className="flex flex-wrap gap-2 mb-4">
        {ingredients.map((name) => (
          <span
            key={name}
            className="inline-flex items-center gap-1 bg-emerald-50 text-emerald-700 px-3 py-1.5 rounded-full text-sm font-medium"
          >
            {name}
            <button
              onClick={() => removeItem(name)}
              className="ml-1 hover:text-red-500 transition-colors cursor-pointer"
              aria-label={`Remove ${name}`}
            >
              ×
            </button>
          </span>
        ))}
      </div>

      <form onSubmit={addItem} className="flex gap-2 mb-5">
        <input
          type="text"
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
          placeholder="Add an ingredient..."
          className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-300"
        />
        <button
          type="submit"
          className="bg-gray-100 text-gray-600 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors cursor-pointer"
        >
          Add
        </button>
      </form>

      <button
        onClick={onGenerate}
        disabled={isGenerating || ingredients.length === 0}
        className="w-full bg-emerald-600 text-white py-3 rounded-xl font-semibold hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors cursor-pointer"
      >
        {isGenerating ? 'Generating Recipes...' : 'Generate Recipes'}
      </button>
    </div>
  );
}
