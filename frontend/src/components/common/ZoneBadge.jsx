/**
 * components/common/ZoneBadge.jsx
 * Displays the current water zone with colour-coded styling.
 */
import React from 'react'
import { getZoneInfo } from '../../utils/zones'

export default function ZoneBadge({ zone, size = 'md' }) {
  const info = getZoneInfo(zone)
  const sizeClass = size === 'lg' ? 'text-lg px-4 py-2' : 'text-sm px-3 py-1'

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full font-semibold ${sizeClass} ${info.bg} ${info.text}`}>
      <span>{info.dot}</span>
      {info.label}
    </span>
  )
}
