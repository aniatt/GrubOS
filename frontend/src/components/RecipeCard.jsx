export default function RecipeCard({ content, isStreaming }) {
  if (!content) return null;

  return (
    <div className="w-full bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">
        Recipes
        {isStreaming && (
          <span className="ml-2 inline-block w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
        )}
      </h2>
      <div className="prose prose-emerald max-w-none text-gray-700 whitespace-pre-wrap text-sm leading-relaxed">
        {content}
      </div>
    </div>
  );
}
