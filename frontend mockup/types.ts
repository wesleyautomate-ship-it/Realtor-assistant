export type View = 'dashboard' | 'tasks' | 'chat' | 'profile';

export interface ActionItem {
    id: 'marketing' | 'analytics' | 'social' | 'strategy' | 'contacts' | 'transactions' | 'playwright';
    title: string;
    subtitle: string;
    color: string;
    icon: JSX.Element;
}

export type ActionId = ActionItem['id'];

export interface ChatMessage {
    id: number;
    text: string;
    sender: 'user' | 'ai';
    suggestions?: string[];
}

export interface Request {
    id: number;
    category: 'Marketing' | 'Sync' | 'Campaign' | 'Data Analysis';
    title: string;
    description: string;
    eta: string;
    status: 'Queued' | 'Processing' | 'Ready for Review';
    progress: number;
    assignees: { id: string, avatarUrl?: string }[];
    image?: string;
    tags?: { text: string; color: string }[];
}

export type Priority = 'Low' | 'Medium' | 'High';

export interface Task {
  id: number;
  title: string;
  dueDate: string;
  priority: Priority;
  isCompleted: boolean;
}