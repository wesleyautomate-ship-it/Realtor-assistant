// Lightweight API layer for social platforms (stubs/mocks)
// Real integrations should securely handle OAuth and tokens on the backend.

export type Platform = 'facebook' | 'instagram' | 'linkedin';

export interface PlatformConnection {
  platform: Platform;
  connected: boolean;
  accountName?: string;
}

export interface ScheduledPost {
  id: string;
  caption: string;
  imageUrl?: string;
  platforms: Platform[];
  scheduledAt: string; // ISO
}

export const socialMediaApi = {
  // Connections (mock)
  async getConnections(): Promise<PlatformConnection[]> {
    return [
      { platform: 'facebook', connected: false },
      { platform: 'instagram', connected: false },
      { platform: 'linkedin', connected: false },
    ];
  },
  async connect(platform: Platform): Promise<PlatformConnection> {
    // In real implementation, redirect to OAuth flow
    return { platform, connected: true, accountName: 'Demo Account' };
  },
  async disconnect(platform: Platform): Promise<PlatformConnection> {
    return { platform, connected: false };
  },

  // Posts (mock)
  async postNow(payload: { caption: string; imageUrl?: string; platforms: Platform[] }): Promise<{ id: string }> {
    console.log('Posting now:', payload);
    return { id: String(Date.now()) };
  },
  async schedule(payload: { caption: string; imageUrl?: string; platforms: Platform[]; scheduledAt: string }): Promise<ScheduledPost> {
    console.log('Scheduling post:', payload);
    return { id: String(Date.now()), ...payload };
  },
  async listScheduled(): Promise<ScheduledPost[]> {
    return [];
  },
};
