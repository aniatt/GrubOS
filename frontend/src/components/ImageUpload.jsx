import { useState, useRef } from 'react';

export default function ImageUpload({ onDetect, isLoading }) {
  const [preview, setPreview] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef(null);

  function handleFile(file) {
    if (!file || !file.type.startsWith('image/')) return;
    setPreview(URL.createObjectURL(file));
    onDetect(file);
  }

  function handleDrop(e) {
    e.preventDefault();
    setDragActive(false);
    handleFile(e.dataTransfer.files[0]);
  }

  function handleDragOver(e) {
    e.preventDefault();
    setDragActive(true);
  }

  return (
    <div className="w-full">
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={() => setDragActive(false)}
        onClick={() => inputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-colors ${
          dragActive
            ? 'border-emerald-400 bg-emerald-50'
            : 'border-gray-300 hover:border-emerald-300 hover:bg-gray-50'
        }`}
      >
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          className="hidden"
          onChange={(e) => handleFile(e.target.files[0])}
        />

        {preview ? (
          <img
            src={preview}
            alt="Uploaded preview"
            className="mx-auto max-h-72 rounded-xl object-contain"
          />
        ) : (
          <div className="py-8">
            <div className="text-5xl mb-3">📷</div>
            <p className="text-lg font-medium text-gray-700">
              Drop a photo of your ingredients
            </p>
            <p className="text-sm text-gray-400 mt-1">
              or click to browse files
            </p>
          </div>
        )}

        {isLoading && (
          <div className="absolute inset-0 bg-white/70 rounded-2xl flex items-center justify-center">
            <div className="flex items-center gap-3 text-emerald-600 font-medium">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
              </svg>
              Detecting ingredients...
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
