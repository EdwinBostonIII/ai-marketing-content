import { useKV } from '@github/spark/hooks'
import { Settings } from './types'

const DEFAULT_SETTINGS: Settings = {
  apiKey: '',
  monthlyBudget: 100,
  webhookUrls: [],
  apiEndpoint: 'http://localhost:8000'
}

export function useSettings() {
  const [settings, setSettings] = useKV<Settings>('app-settings', DEFAULT_SETTINGS)
  
  return { settings, setSettings }
}

export async function createApiRequest(settings: Settings) {
  return async function apiRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers = {
      'Content-Type': 'application/json',
      ...(settings.apiKey && { 'X-API-Key': settings.apiKey }),
      ...options.headers
    }
    
    const response = await fetch(`${settings.apiEndpoint}${endpoint}`, {
      ...options,
      headers
    })
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }))
      throw new Error(error.detail || `API Error: ${response.status}`)
    }
    
    return response.json()
  }
}
