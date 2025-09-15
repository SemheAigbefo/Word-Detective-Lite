export default function HeatLegend() {
  const bands = [
    { label: 'Cold', range: '[0.00–0.25)' },
    { label: 'Cool', range: '[0.25–0.45)' },
    { label: 'Warm', range: '[0.45–0.65)' },
    { label: 'Hot', range: '[0.65–0.80)' },
    { label: 'Very Hot', range: '[0.80–1.00]' },
  ]
  return (
    <div className="legend">
      {bands.map(b => (
        <div key={b.label} className="legend-item">
          <span className={`dot ${b.label.replace(' ','').toLowerCase()}`} aria-hidden>●</span>
          <span className="lbl">{b.label}</span>
          <span className="range">{b.range}</span>
        </div>
      ))}
    </div>
  )
}
