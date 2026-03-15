import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { authApi } from '../services/api'
import useAuthStore from '../store/authStore'

export default function MfaPage() {
  const navigate = useNavigate()
  const { setMfaVerified, logout } = useAuthStore()
  const [code, setCode] = useState('')
  const [attempts, setAttempts] = useState(0)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (code.length !== 6) {
      toast.error('Please enter a 6-digit code.')
      return
    }

    setLoading(true)
    try {
      await authApi.verifyMfa(code)
      setMfaVerified(true)
      toast.success('MFA Verified. Welcome back, Director.')
      navigate('/dashboard')
    } catch (error) {
      const newAttempts = attempts + 1
      setAttempts(newAttempts)

      if (newAttempts >= 3) {
        toast.error('Too many failed attempts. Account locked for this session.')
        // Force logout and clear all local state
        await authApi.logout().catch(() => {})
        logout()
        navigate('/login')
      } else {
        toast.error(`Invalid MFA code. ${3 - newAttempts} attempts remaining.`)
        setCode('')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-blue-900 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <div className="text-4xl mb-4 text-blue-600">🛡️</div>
          <h1 className="text-2xl font-bold text-gray-900">Director Verification</h1>
          <p className="text-sm text-gray-500 mt-2">
            Enter the 6-digit code from your authenticator app.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="flex justify-center">
            <input
              type="text"
              maxLength={6}
              value={code}
              onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
              placeholder="000000"
              className="w-48 text-center text-4xl tracking-widest font-mono border-b-2 border-blue-500 py-2 focus:outline-none bg-transparent"
              autoFocus
            />
          </div>

          <button
            type="submit"
            disabled={loading || code.length !== 6}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg transition disabled:opacity-50"
          >
            {loading ? 'Verifying...' : 'Verify Identity'}
          </button>

          <div className="text-center">
            <button
              type="button"
              onClick={() => {
                logout()
                navigate('/login')
              }}
              className="text-sm text-gray-400 hover:text-gray-600 transition"
            >
              Cancel and Sign Out
            </button>
          </div>
        </form>

        {attempts > 0 && (
          <div className="mt-6 p-3 bg-red-50 rounded-lg text-center">
            <p className="text-xs text-red-600 font-medium">
              Attempt {attempts} of 3. Further failures will result in lockout.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
