"use client"

import { useState } from "react"

export default function CreatorPage() {
  const [inputValue, setInputValue] = useState("")

  const handleCreate = () => {
    // TODO: Implement create functionality
    console.log("Creating:", inputValue)
  }

  // create a Booklet
  // create TextBlocks within in a Booklet
  return (
    <div className="container mx-auto p-8">
      <h1 className="text-2xl font-bold mb-6">Creator: create booklets and text blocks</h1>
      <div className="max-w-md mx-auto">
        <div className="mb-4">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Enter your text here (English/Chinese)"
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={10}
          />
        </div>
        <button
          onClick={handleCreate}
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors"
        >
          Create text block
        </button>
      </div>
    </div>
  )
}