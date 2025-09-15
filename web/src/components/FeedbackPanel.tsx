type Guess = {
  normalizedWord: string
  similarity: number
  band: 'Cold'|'Cool'|'Warm'|'Hot'|'Very Hot'
  isCorrect: boolean
  at: string
}

export default function FeedbackPanel({ last, error }: { last?: Guess, error?: any }) {
  return (
    <div className="panel" aria-live="polite">
      {error?.error ? (
        <div className="error">{error.error.message}</div>
      ) : last ? (
        <div>
          <div><strong>{last.normalizedWord}</strong> → <span className={`badge ${last.band.replace(' ','').toLowerCase()}`}>{last.band}</span></div>
          <div>Similarity: {last.similarity.toFixed(4)} {last.isCorrect && '✓'}</div>
        </div>
      ) : (
        <div>Make a guess to see feedback.</div>
      )}
    </div>
  )
}
