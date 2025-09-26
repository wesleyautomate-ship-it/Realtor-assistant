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
export type View = 'dashboard' | 'tasks' | 'chat' | 'properties' | 'content' | 'analytics' | 'workflows' | 'transactions';

export type TransactionStatus = 'draft' | 'in_progress' | 'pending_approval' | 'completed' | 'cancelled';
export type MilestoneType = 'offer_submitted' | 'offer_accepted' | 'contract_signed' | 'inspection' | 'appraisal' | 'financing_approved' | 'closing' | 'possession';

export interface Milestone {
  id: string;
  type: MilestoneType;
  title: string;
  description: string;
  dueDate: string;
  completed: boolean;
  completedAt?: string;
  documents?: string[];
}

export interface Document {
  id: string;
  name: string;
  type: string;
  url: string;
  uploadedAt: string;
  size: number;
}

export interface Transaction {
  id: string;
  propertyId: string;
  clientId: string;
  status: TransactionStatus;
  offerAmount: number;
  salePrice?: number;
  createdAt: string;
  updatedAt: string;
  milestones: Milestone[];
  documents: Document[];
  notes: string;
  agentId: string;
  expectedClosingDate: string;
  actualClosingDate?: string;
}

export interface TransactionTemplate {
  id: string;
  name: string;
  subject: string;
  body: string;
  milestoneTypes: MilestoneType[];
  isDefault: boolean;
  createdAt: string;
  updatedAt: string;
}
export type ActionId = 'workflows' | 'marketing' | 'social' | 'contacts' | 'playwright' | 'properties' | 'content' | 'analytics' | 'transactions';

export interface Task {
  id: string;
  title: string;
  status: 'pending' | 'in_progress' | 'completed';
  dueDate?: string;
}
