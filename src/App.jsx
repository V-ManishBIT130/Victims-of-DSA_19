import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { apiCall, API_ENDPOINTS } from './config/api'

function App() {
  const [count, setCount] = useState(0)
  const [backendStatus, setBackendStatus] = useState({
    connected: false,
    loading: true,
    message: '',
    data: null
  })

  // Test backend connection
  useEffect(() => {
    const testBackendConnection = async () => {
      try {
        const data = await apiCall(API_ENDPOINTS.TEST)
        
        if (data.success) {
          setBackendStatus({
            connected: true,
            loading: false,
            message: data.message,
            data: data.data
          })
        }
      } catch (error) {
        setBackendStatus({
          connected: false,
          loading: false,
          message: 'Failed to connect to backend',
          data: null
        })
      }
    }

    testBackendConnection()
  }, [])

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      
      {/* Backend Connection Status */}
      <div className="card" style={{ 
        backgroundColor: backendStatus.connected ? '#1a472a' : '#472a1a',
        border: `2px solid ${backendStatus.connected ? '#4ade80' : '#f87171'}`
      }}>
        <h3>Backend Connection Status</h3>
        {backendStatus.loading ? (
          <p>⏳ Testing connection...</p>
        ) : backendStatus.connected ? (
          <div>
            <p style={{ color: '#4ade80' }}>✅ {backendStatus.message}</p>
            {backendStatus.data && (
              <div style={{ fontSize: '0.9em', marginTop: '10px' }}>
                <p>Server: {backendStatus.data.server}</p>
                <p>Database: {backendStatus.data.database}</p>
                <p>Port: {backendStatus.data.port}</p>
              </div>
            )}
          </div>
        ) : (
          <p style={{ color: '#f87171' }}>❌ {backendStatus.message}</p>
        )}
      </div>

      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
