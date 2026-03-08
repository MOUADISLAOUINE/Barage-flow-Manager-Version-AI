import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'react-hot-toast'
import useAuthStore from './store/authStore'

// Pages
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import ReleaseOrdersPage from './pages/ReleaseOrdersPage'
import ForecastPage from './pages/ForecastPage'
import CooperativesPage from './pages/CooperativesPage'
import AuditLogPage from './pages/AuditLogPage'
import AdminPage from './pages/AdminPage'
import NotFoundPage from './pages/NotFoundPage'

// Layout
import AppLayout from './components/common/AppLayout'

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: 1, staleTime: 30_000 } },
})

function ProtectedRoute({ children, roles }) {
  const { isAuthenticated, role } = useAuthStore()
  if (!isAuthenticated()) return <Navigate to="/login" replace />
  if (roles && !roles.includes(role)) return <Navigate to="/dashboard" replace />
  return children
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Toaster position="top-right" />
        <Routes>
          <Route path="/login" element={<LoginPage />} />

          <Route path="/" element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          }>
            <Route index element={<Navigate to="/dashboard" replace />} />

            {/* Water data — Directors, Operators, Officers */}
            <Route path="dashboard" element={
              <ProtectedRoute roles={['DIRECTOR', 'OPERATOR', 'AGRICULTURAL_OFFICER']}>
                <DashboardPage />
              </ProtectedRoute>
            } />
            <Route path="forecast" element={
              <ProtectedRoute roles={['DIRECTOR', 'OPERATOR', 'AGRICULTURAL_OFFICER']}>
                <ForecastPage />
              </ProtectedRoute>
            } />
            <Route path="cooperatives" element={
              <ProtectedRoute roles={['DIRECTOR', 'OPERATOR', 'AGRICULTURAL_OFFICER']}>
                <CooperativesPage />
              </ProtectedRoute>
            } />

            {/* Release orders — Directors and Operators only */}
            <Route path="orders" element={
              <ProtectedRoute roles={['DIRECTOR', 'OPERATOR']}>
                <ReleaseOrdersPage />
              </ProtectedRoute>
            } />

            {/* Audit log — Directors and Admins */}
            <Route path="audit" element={
              <ProtectedRoute roles={['DIRECTOR', 'ADMIN']}>
                <AuditLogPage />
              </ProtectedRoute>
            } />

            {/* Admin — Admin only */}
            <Route path="admin" element={
              <ProtectedRoute roles={['ADMIN']}>
                <AdminPage />
              </ProtectedRoute>
            } />
          </Route>

          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
