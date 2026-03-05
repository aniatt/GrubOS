import { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import IngredientList from './components/IngredientList';
import RecipeCard from './components/RecipeCard';
import { detectIngredients, generateRecipes } from './api/client';

export default function App() {
  const [ingredients, setIngredients] = useState([]);
  const [isDetecting, setIsDetecting] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [recipeContent, setRecipeContent] = useState('');
  const [error, setError] = useState(null);

  async function handleDetect(file) {
    setError(null);
    setIsDetecting(true);
    setRecipeContent('');
    try {
      const data = await detectIngredients(file);
      const names = [...new Set(data.ingredients.map((i) => i.name))];
      setIngredients(names);
    } catch (err) {
      setError(`Detection failed: ${err.message}`);
    } finally {
      setIsDetecting(false);
    }
  }

  async function handleGenerate() {
    setError(null);
    setIsGenerating(true);
    setRecipeContent('');
    try {
      const body = await generateRecipes(ingredients);
      const reader = body.getReader();
      const decoder = new TextDecoder();
      let text = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        text += decoder.decode(value, { stream: true });
        setRecipeContent(text);
      }
    } catch (err) {
      setError(`Recipe generation failed: ${err.message}`);
    } finally {
      setIsGenerating(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-100">
        <div className="max-w-3xl mx-auto px-4 py-5 flex items-center gap-3">
          <span className="text-3xl">🍳</span>
          <div>
            <h1 className="text-xl font-bold text-gray-900">GrubOS</h1>
            <p className="text-sm text-gray-500">
              Snap your ingredients, get recipes instantly
            </p>
          </div>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-8 flex flex-col gap-6">
        <ImageUpload onDetect={handleDetect} isLoading={isDetecting} />

        {error && (
          <div className="bg-red-50 text-red-700 px-4 py-3 rounded-xl text-sm">
            {error}
          </div>
        )}

        <IngredientList
          ingredients={ingredients}
          setIngredients={setIngredients}
          onGenerate={handleGenerate}
          isGenerating={isGenerating}
        />

        <RecipeCard content={recipeContent} isStreaming={isGenerating} />
      </main>
    </div>
  );
}
