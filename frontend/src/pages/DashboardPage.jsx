/**
 * pages/DashboardPage.jsx
 * Live dam status dashboard — water level, zone, alerts.
 * Accessible to: Director, Operator, Agricultural Officer.
 */
import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { damApi } from '../services/api'
import ZoneBadge from '../components/common/ZoneBadge'
import { formatM3, formatPct } from '../utils/zones'

export default function DashboardPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['dam-status'],
    queryFn: () => damApi.getStatus().then((r) => r.data),
    refetchInterval: 60_000, // Refresh every 60s (sensors read every 15 min)
  })

  if (isLoading) return <p className="p-6 text-gray-500">Loading dam status…</p>
  if (error) return <p className="p-6 text-red-500">Failed to load dam status.</p>

  const dam = data

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">{dam.name}</h1>
        <ZoneBadge zone={dam.current_zone} size="lg" />
      </div>

      {/* Safety lock banner */}
      {dam.safety_lock_active && (
        <div className="rounded-lg bg-red-50 border border-red-300 p-4 flex items-center gap-3">
          <span className="text-2xl">🔐</span>
          <div>
            <p className="font-bold text-red-800">Safety Lock Active</p>
            <p className="text-red-700 text-sm">
              All water releases are blocked. Director MFA override required.
            </p>
          </div>
        </div>
      )}

      {/* Stats grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatCard
          label="Current Level"
          value={formatPct(dam.current_level_pct)}
          sub={formatM3(dam.current_level_m3)}
        />
        <StatCard
          label="Total Capacity"
          value={formatM3(dam.max_capacity_m3)}
        />
        <StatCard
          label="Safety Reserve"
          value={formatPct(dam.safety_reserve_pct)}
          sub="Minimum threshold"
        />
      </div>

      {/* Water level bar */}
      <div>
        <div className="flex justify-between text-sm text-gray-600 mb-1">
          <span>0%</span>
          <span>Safety Reserve ({formatPct(dam.safety_reserve_pct)})</span>
          <span>100%</span>
        </div>
        <div className="h-6 bg-gray-200 rounded-full overflow-hidden relative">
          {/* Safety reserve marker */}
          <div
            className="absolute top-0 bottom-0 w-0.5 bg-red-500 z-10"
            style={{ left: `${dam.safety_reserve_pct}%` }}
          />
          {/* Level bar */}
          <div
            className="h-full rounded-full transition-all duration-700"
            style={{
              width: `${dam.current_level_pct}%`,
              backgroundColor: dam.safety_lock_active ? '#ef4444' :
                               dam.current_zone === 'WARNING' ? '#f97316' :
                               dam.current_zone === 'ALERT' ? '#eab308' : '#22c55e',
            }}
          />
        </div>
      </div>

      <p className="text-xs text-gray-400">
        Last reading: {new Date(dam.last_reading_at).toLocaleString()}
      </p>
    </div>
  )
}

function StatCard({ label, value, sub }) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="mt-1 text-2xl font-bold text-gray-900">{value}</p>
      {sub && <p className="text-xs text-gray-400 mt-0.5">{sub}</p>}
    </div>
  )
}
