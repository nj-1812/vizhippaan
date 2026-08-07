const API = process.env.NEXT_PUBLIC_API_URL ?? 'http://127.0.0.1:8000/api'

async function request<T = any>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API}${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...(init?.headers ?? {}) },
    cache: 'no-store',
  })
  if (!response.ok) throw new Error(await response.text())
  return response.json()
}

export const vizApi = {
  health: () => request('/health'),
  overview: (district = 'All Districts') => request(`/dashboard/overview?district=${encodeURIComponent(district)}`),
  summary: (district = 'All Districts') => request(`/dashboard/summary?district=${encodeURIComponent(district)}`),
  trend: () => request('/dashboard/risk-trend'),
  factors: () => request('/dashboard/top-risk-factors'),
  alerts: () => request('/dashboard/alerts'),
  student: (id: string) => request(`/students/${encodeURIComponent(id)}`),
  risk: (id: string) => request(`/students/${encodeURIComponent(id)}/risk`),
  explanation: (id: string) => request(`/students/${encodeURIComponent(id)}/explanation`),
  digitalTwin: (id: string) => request(`/students/${encodeURIComponent(id)}/digital-twin`),
  districts: () => request('/districts/risk'),
  fairness: () => request('/fairness/report'),
  opportunities: () => request('/opportunities'),
  quality: () => request('/quality'),
  simulateIntervention: (studentId: string, interventions: string[]) => request('/interventions/simulate', {
    method: 'POST', body: JSON.stringify({ student_id: studentId, interventions }),
  }),
}
