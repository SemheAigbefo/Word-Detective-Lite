export default function TrendChart({ values }: { values: number[] }) {
  if (!values.length) return null
  const w = 240, h = 60, pad = 8
  const min = Math.min(...values, 0)
  const max = Math.max(...values, 1)
  const pts = values.map((v, i) => {
    const x = pad + (i * (w - 2*pad)) / Math.max(1, values.length - 1)
    const y = h - pad - ((v - min) / Math.max(0.0001, (max - min))) * (h - 2*pad)
    return `${x},${y}`
  }).join(' ')
  return (
    <svg width={w} height={h} role="img" aria-label="Similarity trend">
      <polyline fill="none" stroke="currentColor" strokeWidth="2" points={pts} />
    </svg>
  )
}
