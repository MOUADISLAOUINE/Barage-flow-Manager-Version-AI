/**
 * store/authStore.js
 * Global auth state: current user, JWT token, role.
 */
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      role: null,
      mfaPending: false,
      tempToken: null,

      setAuth: ({ token, role }) => set({ token, role, mfaPending: false, tempToken: null }),

      setMfaPending: ({ tempToken, role }) => set({ mfaPending: true, tempToken, role }),

      logout: () => set({ user: null, token: null, role: null, mfaPending: false, tempToken: null }),

      isAuthenticated: () => !!get().token,

      isDirector: () => get().role === 'DIRECTOR',
      isOperator: () => get().role === 'OPERATOR',
      isOfficer: () => get().role === 'AGRICULTURAL_OFFICER',
      isAdmin: () => get().role === 'ADMIN',

      // Permission helpers matching the permission table in the team guide
      canApproveOrders: () => get().role === 'DIRECTOR',
      canSubmitOrders: () => ['DIRECTOR', 'OPERATOR'].includes(get().role),
      canViewWaterData: () => ['DIRECTOR', 'OPERATOR', 'AGRICULTURAL_OFFICER'].includes(get().role),
      canOverrideSafetyLock: () => get().role === 'DIRECTOR',
      canManageUsers: () => get().role === 'ADMIN',
    }),
    { name: 'bfm-auth' }
  )
)

export default useAuthStore
