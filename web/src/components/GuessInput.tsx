import { useEffect, useRef, useState } from 'react'

export default function GuessInput({ onSubmit }: { onSubmit: (word: string) => void }) {
  const [value, setValue] = useState('')
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  return (
    <form
      className="guess"
      onSubmit={(e) => {
        e.preventDefault()
        const v = value.trim()
        if (v) onSubmit(v)
        setValue('')
        inputRef.current?.focus()
      }}
    >
      <input
        ref={inputRef}
        aria-label="Enter a guess"
        value={value}
        onChange={e => setValue(e.target.value)}
      />
      <button type="submit">Guess</button>
    </form>
  )
}
