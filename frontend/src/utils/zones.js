/**
 * utils/zones.js
 * Helper utilities for water zone display — colours, labels, icons.
 */

export const ZONES = {
  NORMAL:   { label: 'Normal',   colour: '#22c55e', bg: 'bg-green-100',  text: 'text-green-800',  dot: '🟢' },
  ALERT:    { label: 'Alert',    colour: '#eab308', bg: 'bg-yellow-100', text: 'text-yellow-800', dot: '🟡' },
  WARNING:  { label: 'Warning',  colour: '#f97316', bg: 'bg-orange-100', text: 'text-orange-800', dot: '🟠' },
  CRITICAL: { label: 'Critical', colour: '#ef4444', bg: 'bg-red-100',    text: 'text-red-800',    dot: '🔴' },
}

export function getZoneInfo(zone) {
  return ZONES[zone] ?? ZONES.NORMAL
}

export function formatM3(value) {
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(2)} MCM`
  if (value >= 1_000) return `${(value / 1_000).toFixed(1)} k m³`
  return `${value.toFixed(0)} m³`
}

export function formatPct(value) {
  return `${value.toFixed(1)}%`
}
