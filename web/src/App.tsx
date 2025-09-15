import { useState, useMemo } from 'react'
import { useCreateGame, useGame, useSubmitGuess } from './hooks/useGame'
import GuessInput from './components/GuessInput'
import FeedbackPanel from './components/FeedbackPanel'
import HistoryList from './components/HistoryList'
import HeatLegend from './components/HeatLegend'
import TrendChart from './components/TrendChart'

export default function App() {
  const [mode, setMode] = useState<'daily' | 'free'>('daily')
  const [gameId, setGameId] = useState<string | null>(null)
  const createGame = useCreateGame()
  const { data: game } = useGame(gameId)
  const submitGuess = useSubmitGuess()

  const last = useMemo(() => game?.lastGuesses?.[0], [game])

  return (
    <div className="container">
      <h1>Word Detective Lite</h1>
      <p className="tagline">Guess the target word by similarity bands.</p>

      <div className="controls">
        <label>
          Mode:&nbsp;
          <select value={mode} onChange={e => setMode(e.target.value as any)}>
            <option value="daily">Daily</option>
            <option value="free">Free Play</option>
          </select>
        </label>
        <button
          onClick={async () => {
            const g = await createGame.mutateAsync({ mode })
            setGameId(g.gameId)
          }}
        >
          Start
        </button>
      </div>

      {gameId && (
        <>
          <GuessInput
            onSubmit={async (word) => {
              if (!gameId) return
              try {
                await submitGuess.mutateAsync({ gameId, word })
              } catch (e) {
                // handled via error shape in panel
              }
            }}
          />
          <FeedbackPanel last={last} error={submitGuess.error as any} />
          <HeatLegend />
          <HistoryList guesses={game?.lastGuesses ?? []} />
          <TrendChart values={(game?.lastGuesses ?? []).map(g => g.similarity).reverse()} />
        </>
      )}

      <footer>
        <small>CPU-only • Anonymous sessions • No auth</small>
      </footer>
    </div>
  )
}
