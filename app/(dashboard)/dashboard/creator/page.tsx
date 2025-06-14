"use client";

import { useState } from "react";

export default function CreatorPage() {
  const [inputValue, setInputValue] = useState("");

  const handleCreate = () => {
    // TODO: Implement create functionality
    console.log("Creating:", inputValue);
  };

  // create a Booklet
  // create TextBlocks within in a Booklet
  return (
    <div className="container mx-auto p-8">
      <h1 className="text-2xl font-bold mb-6">
        Creator: create booklets and text blocks
      </h1>
      <div className="max-w-lg w-4/5 flex flex-col flex-wrap items-start justify-items-start">
        <div className="mb-4 w-full">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Enter your markdown here"
            className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm bg-gray-50"
            rows={15}
          />
        </div>
        <button
          onClick={handleCreate}
          className="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors font-medium"
        >
          Create Booklet
        </button>
      </div>
    </div>
  );
}
