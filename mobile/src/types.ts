export type AIProvider = 'openai' | 'gemini';

export interface AIContentRequest {
  prompt: string;
  contentType?: 'description' | 'social' | 'email' | 'brochure';
  tone?: 'professional' | 'casual' | 'luxury' | 'friendly';
}

export interface AIContentResponse {
  content: string;
  contentType: 'description' | 'social' | 'email' | 'brochure';
  tone?: 'professional' | 'casual' | 'luxury' | 'friendly';
  wordCount?: number;
  suggestions?: string[];
}

// Mobile UI Types (mirroring frontend mockup)
export type View = 'dashboard' | 'tasks' | 'chat' | 'properties' | 'content' | 'analytics' | 'workflows';
export type ActionId = 'workflows' | 'marketing' | 'social' | 'contacts' | 'playwright' | 'properties' | 'content' | 'analytics';

export interface Task {
  id: string;
  title: string;
  status: 'pending' | 'in_progress' | 'completed';
  dueDate?: string;
}
