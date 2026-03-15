import React from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import useAuthStore from '../../store/authStore'

export default function ProtectedRoute({ children, roles }) {
  const { isAuthenticated, role, mfaVerified } = useAuthStore()
  const location = useLocation()

  // 1. Not logged in at all
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace state={{ from: location }} />
  }

  // 2. Director MFA Check
  // The role is normalized to uppercase in the auth store.
  if (role === 'DIRECTOR' && !mfaVerified && location.pathname !== '/mfa') {
    return <Navigate to="/mfa" replace />
  }

  // 3. Role-based access control
  if (roles && !roles.includes(role)) {
    // If they are logged in but unauthorized for this specific page, send to a safe place
    return <Navigate to="/dashboard" replace />
  }

  // 4. Authorized
  return children
}
