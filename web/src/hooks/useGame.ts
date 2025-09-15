import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import api from '../api/client'

export function useCreateGame() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ mode }: { mode: 'daily'|'free' }) => api.createGame(mode),
    onSuccess: (game) => {
      qc.invalidateQueries({ queryKey: ['game', game.gameId] })
    }
  })
}

export function useGame(gameId: string | null) {
  return useQuery({
    enabled: !!gameId,
    queryKey: ['game', gameId],
    queryFn: () => api.getGame(gameId!),
    refetchInterval: 2000
  })
}

export function useSubmitGuess() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ gameId, word }: { gameId: string, word: string }) => api.submitGuess(gameId, word),
    onSuccess: (_data, vars) => {
      qc.invalidateQueries({ queryKey: ['game', vars.gameId] })
    }
  })
}
