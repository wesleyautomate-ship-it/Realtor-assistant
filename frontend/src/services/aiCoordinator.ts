// Simple AI coordinator service to centralize AI features across modules
// This is a front-end stub. Replace with real backend/OpenAI calls in Alpha-2.

import { ChatMessage } from "../types";

type MetricsEvent = {
  type: "request" | "response" | "error";
  timestamp: number;
  latencyMs?: number;
  tokensIn?: number;
  tokensOut?: number;
  module?: string;
};

export type AIContext = {
  module?: "property" | "crm" | "marketing" | "social" | "strategy" | "packages" | "analytics";
  entityId?: string;
};

export type AIRequest = {
  prompt: string;
  context?: AIContext;
};

export type AIResponse = Omit<ChatMessage, "id" | "sender"> & {
  // enrich as needed
};

const subscribers = new Set<(event: MetricsEvent) => void>();

function emit(event: MetricsEvent) {
  subscribers.forEach((cb) => {
    try { cb(event); } catch {}
  });
}

export function subscribeMetrics(cb: (event: MetricsEvent) => void) {
  subscribers.add(cb);
  return () => subscribers.delete(cb);
}

export async function sendMessage(req: AIRequest): Promise<AIResponse> {
  const start = performance.now();
  emit({ type: "request", timestamp: Date.now(), module: req.context?.module });

  // Simulated routing by module with contextual actions
  const lower = req.prompt.toLowerCase();
  const isCMA = lower.includes("cma") || lower.includes("analysis");
  const isEmail = lower.includes("email") || lower.includes("follow-up");
  const isSocial = lower.includes("social") || lower.includes("post");

  // Generate a rich markdown response with actions
  let response: AIResponse = {
    text: `# Assistant Response\n\nI've analyzed your request. Choose a next step or refine your prompt.\n\n## Suggestions\n- Generate content\n- Analyze market data\n- Draft a client message`,
    format: "markdown",
    suggestions: [
      "Show me my tasks",
      "Analyze market trends",
      "Create a social post",
    ],
    actions: [
      { label: "📊 Run CMA Insights", prompt: "Generate CMA insights for selected property" },
      { label: "📝 Draft Client Email", prompt: "Draft a follow-up email to the lead about viewing" },
      { label: "📱 Create Social Post", prompt: "Create an Instagram post highlighting property features" },
    ],
  };

  if (isCMA) {
    response = {
      text: `# CMA Insights\n\n- Pricing band: AED 3.2M–3.6M\n- Days on market median: 42\n- Recommended list: AED 3.4M\n\n## Next actions\n- Prepare brochure\n- Draft owner update\n- Schedule open house`,
      format: "markdown",
      suggestions: ["Prepare brochure", "Draft owner update", "Schedule open house"],
      actions: [
        { label: "📄 Create Brochure", prompt: "Create a brochure using Beta-3 templates" },
        { label: "📧 Owner Update Email", prompt: "Draft an owner update email summarizing CMA" },
        { label: "📅 Open House Plan", prompt: "Propose an open house plan and checklist" },
      ],
    };
  } else if (isEmail) {
    response = {
      text: `## Email Draft\n\nHi [Client Name],\n\nFollowing up regarding the property viewing you requested...\n\n— Regards,`,
      format: "markdown",
      suggestions: ["Personalize with client details", "Add next available times"],
      actions: [
        { label: "🔍 Personalize", prompt: "Personalize with CRM data for this client" },
        { label: "⏰ Propose Times", prompt: "Suggest next 3 available times from my calendar" },
      ],
    };
  } else if (isSocial) {
    response = {
      text: `## Social Post\n\nExperience luxury living at Seven Palm! 🌴\n\n- 2BR | 1,200 sqft\n- City views, premium finishes\n\n#DubaiRealEstate #LuxuryLiving`,
      format: "markdown",
      suggestions: ["Add hashtags", "Create variants"],
      actions: [
        { label: "🏷️ Optimize Hashtags", prompt: "Optimize hashtags for Instagram and LinkedIn" },
        { label: "🗓️ Schedule Post", prompt: "Schedule for Fri 10:00 and cross-post" },
      ],
    };
  }

  // Simulate latency
  await new Promise((r) => setTimeout(r, 600));
  const end = performance.now();
  emit({ type: "response", timestamp: Date.now(), latencyMs: end - start, module: req.context?.module });
  return response;
}

export default { sendMessage, subscribeMetrics };
