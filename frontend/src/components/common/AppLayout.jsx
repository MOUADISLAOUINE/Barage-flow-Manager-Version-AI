import React from 'react'
import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import useAuthStore from '../../store/authStore'
import { authApi } from '../../services/api'
import toast from 'react-hot-toast'

const navItems = [
  { to: '/dashboard',      label: 'Dashboard',      icon: '📊', roles: ['DIRECTOR','OPERATOR','AGRICULTURAL_OFFICER'] },
  { to: '/forecast',       label: 'Forecast',        icon: '🔮', roles: ['DIRECTOR','OPERATOR','AGRICULTURAL_OFFICER'] },
  { to: '/cooperatives',   label: 'Cooperatives',    icon: '🌾', roles: ['DIRECTOR','OPERATOR','AGRICULTURAL_OFFICER'] },
  { to: '/orders',         label: 'Release Orders',  icon: '💧', roles: ['DIRECTOR','OPERATOR'] },
  { to: '/audit',          label: 'Audit Log',       icon: '📋', roles: ['DIRECTOR','ADMIN'] },
  { to: '/admin',          label: 'Admin',           icon: '⚙️',  roles: ['ADMIN'] },
]

export default function AppLayout() {
  const { role, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = async () => {
    try { await authApi.logout() } catch {}
    logout()
    navigate('/login')
    toast.success('Logged out.')
  }

  const visible = navItems.filter((item) => item.roles.includes(role))

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="w-56 bg-blue-900 text-white flex flex-col">
        <div className="p-5 border-b border-blue-800">
          <div className="text-xl font-bold">💧 Barrage-Flow</div>
          <div className="text-xs text-blue-300 mt-0.5">Tiznit Dam System</div>
        </div>

        <nav className="flex-1 p-3 space-y-1">
          {visible.map((item) => (
            <NavLink
              key={item.to} to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition ${
                  isActive ? 'bg-blue-700 text-white' : 'text-blue-200 hover:bg-blue-800 hover:text-white'
                }`
              }
            >
              <span>{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="p-3 border-t border-blue-800">
          <div className="text-xs text-blue-400 mb-2 px-2">{role}</div>
          <button
            onClick={handleLogout}
            className="w-full text-left px-3 py-2 rounded-lg text-sm text-blue-200 hover:bg-blue-800 hover:text-white transition"
          >
            🚪 Sign out
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  )
}
