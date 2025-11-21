import React from 'react';

function SchemaMarkup({ schema }) {
  if (!schema || !schema.json_ld) {
    return null;
  }

  const copyToClipboard = () => {
    navigator.clipboard.writeText(schema.json_ld);
    alert('Schema markup copied to clipboard');
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 border border-slate-100 mt-8">
      <div className="flex justify-between items-start mb-6">
        <div>
          <h3 className="text-2xl font-bold text-slate-800 mb-2">Schema Markup Generator</h3>
          <p className="text-slate-600">Auto-generated JSON-LD schema for better search visibility</p>
        </div>
        <span className="px-4 py-2 bg-blue-100 text-blue-700 rounded-lg font-medium">
          {schema.content_type}
        </span>
      </div>

      <div className="bg-slate-50 rounded-lg border border-slate-200 p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <h4 className="font-semibold text-slate-700">JSON-LD Code</h4>
          <button
            onClick={copyToClipboard}
            className="px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-medium hover:shadow-lg transition-all active:scale-95"
          >
            Copy Code
          </button>
        </div>
        
        <pre className="bg-slate-900 text-green-400 p-4 rounded-lg overflow-x-auto text-sm font-mono">
          {schema.json_ld}
        </pre>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-semibold text-blue-900 mb-2">Implementation Instructions</h4>
        <ol className="text-sm text-blue-800 space-y-2 list-decimal list-inside">
          <li>Copy the JSON-LD code above</li>
          <li>Add it to your HTML within a {'<script type="application/ld+json">'} tag</li>
          <li>Place it in the {'<head>'} section or before the closing {'</body>'} tag</li>
          <li>Validate using Google's Rich Results Test</li>
        </ol>
      </div>
    </div>
  );
}

export default SchemaMarkup;
