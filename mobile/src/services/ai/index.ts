import { CONFIG } from '../../config';
import type { AIProvider } from '../../types';
import { apiPost } from '../api';
import type { AIContentRequest, AIContentResponse } from '../../types';

// Prefer calling the backend which securely talks to providers.
// The backend should accept a provider query or body field.

export async function generateContent(req: AIContentRequest, provider?: AIProvider): Promise<AIContentResponse> {
  const selected = provider || CONFIG.aiProvider;
  return apiPost<AIContentResponse>(`/ai/generate-content?provider=${selected}`, req);
}

export async function analyzeProperty(req: { description: string; details?: Record<string, unknown> }, provider?: AIProvider) {
  const selected = provider || CONFIG.aiProvider;
  return apiPost<any>(`/ai/analyze-property?provider=${selected}`, req);
}
