import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [duration, setDuration] = useState('')
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)

  const API_URL = 'http://127.0.0.1:5000'

  const predictViews = async () => {
    setLoading(true)
    setPrediction(null)

    const res = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ duration: Number(duration) })
    })

    const data = await res.json()
    setPrediction(data.predicted_views)
    setLoading(false)
  }

  return (
    <>
      <div>
        <img src={viteLogo} className="logo" />
        <img src={reactLogo} className="logo react" />
      </div>

      <h1>YouTube AI View Predictor</h1>

      <div className="card">
        <input
          type="number"
          placeholder="Video duration (seconds)"
          value={duration}
          onChange={(e) => setDuration(e.target.value)}
        />

        <button onClick={predictViews} disabled={!duration || loading}>
          {loading ? 'Predicting...' : 'Predict Views'}
        </button>

        {prediction !== null && (
          <p>
            📈 Predicted Views: <strong>{prediction}</strong>
          </p>
        )}
      </div>

      <h2>AI Trend Graph</h2>
      <img
        src={`${API_URL}/plot`}
        alt="AI Trend"
        style={{ width: '100%', maxWidth: '800px', borderRadius: '10px' }}
      />
    </>
  )
}

export default App
