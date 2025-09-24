import { CONFIG } from '../config';

export async function apiPost<T>(path: string, body: unknown, init?: RequestInit): Promise<T> {
  const res = await fetch(`${CONFIG.apiBaseUrl}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {})
    },
    body: JSON.stringify(body),
    ...init,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API POST ${path} failed: ${res.status} ${res.statusText} - ${text}`);
  }
  return res.json();
}

export async function apiGet<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${CONFIG.apiBaseUrl}${path}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {})
    },
    ...init,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API GET ${path} failed: ${res.status} ${res.statusText} - ${text}`);
  }
  return res.json();
}
