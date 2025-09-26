// Simple in-memory workflow engine for Packages (B4-B)
// In production, this would call Alpha-2 orchestration APIs.

import type { PackageDefinition } from '../utils/packageOrchestration';

export type RunStatus = 'queued' | 'running' | 'completed' | 'failed';
export type StepStatus = 'pending' | 'running' | 'completed' | 'failed';

export interface WorkflowStepRun {
  id: string;
  title: string;
  status: StepStatus;
  logs: string[];
}

export interface WorkflowRun {
  id: string;
  packageId: string;
  packageName: string;
  status: RunStatus;
  startedAt: string;
  completedAt?: string;
  steps: WorkflowStepRun[];
  context?: Record<string, any>;
}

const runs: WorkflowRun[] = [];

export function listRuns(): WorkflowRun[] {
  return [...runs].sort((a, b) => (b.startedAt.localeCompare(a.startedAt)));
}

export function getRun(id: string): WorkflowRun | undefined {
  return runs.find(r => r.id === id);
}

export async function startRun(pkg: PackageDefinition, context?: Record<string, any>): Promise<WorkflowRun> {
  const run: WorkflowRun = {
    id: `run_${Date.now()}`,
    packageId: pkg.id,
    packageName: pkg.name,
    status: 'queued',
    startedAt: new Date().toISOString(),
    steps: pkg.steps.map(s => ({ id: s.id, title: s.title, status: 'pending', logs: [] })),
    context,
  };
  runs.unshift(run);
  // simulate async process
  queueMicrotask(() => executeRun(run.id));
  return run;
}

export async function executeRun(runId: string) {
  const run = getRun(runId);
  if (!run) return;
  run.status = 'running';
  for (const step of run.steps) {
    step.status = 'running';
    step.logs.push(`[${new Date().toISOString()}] Started ${step.title}`);
    // Simulate work
    await new Promise(res => setTimeout(res, 400));
    step.logs.push(`[${new Date().toISOString()}] Completed ${step.title}`);
    step.status = 'completed';
  }
  run.status = 'completed';
  run.completedAt = new Date().toISOString();
}
