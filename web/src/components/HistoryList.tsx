type Guess = {
  normalizedWord: string
  similarity: number
  band: 'Cold'|'Cool'|'Warm'|'Hot'|'Very Hot'
  isCorrect: boolean
  at: string
}

export default function HistoryList({ guesses }: { guesses: Guess[] }) {
  return (
    <div className="history">
      <h3>Last 10 Guesses</h3>
      <ul>
        {guesses.map((g, i) => (
          <li key={i}>
            <span className={`dot ${g.band.replace(' ','').toLowerCase()}`} aria-hidden>●</span>
            <span className="word">{g.normalizedWord}</span>
            <span className="sim">{g.similarity.toFixed(3)}</span>
            <span className="band">{g.band}</span>
            {g.isCorrect && <span className="ok">✓</span>}
          </li>
        ))}
      </ul>
    </div>
  )
}
