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
      mfaVerified: false,

      // Normalize role to uppercase to avoid casing bugs during comparisons
      setAuth: ({ token, role }) => set({ 
        token, 
        role: role.toUpperCase(), 
        mfaVerified: role.toUpperCase() !== 'DIRECTOR' 
      }),

      setMfaVerified: (status) => set({ mfaVerified: status }),

      logout: () => set({ user: null, token: null, role: null, mfaVerified: false }),

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
