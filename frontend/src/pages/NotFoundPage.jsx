// pages/NotFoundPage.jsx
import React from 'react'
import { Link } from 'react-router-dom'
export default function NotFoundPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center p-8">
      <div className="text-6xl mb-4">💧</div>
      <h1 className="text-3xl font-bold text-gray-900">404 — Page Not Found</h1>
      <Link to="/dashboard" className="mt-6 text-blue-600 underline">Back to Dashboard</Link>
    </div>
  )
}
