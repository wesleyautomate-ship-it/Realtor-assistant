# Analytics and KPIs

Source: Target Tech Spec + repo review.

## KPI Categories
- Product usage
  - Daily/weekly active users, session length, feature adoption
- Operational
  - API latency (p50/p90/p95), error rate, uptime, queue length
- Business
  - Lead conversion rate, response time to leads, content volume
- Quality
  - AI content satisfaction score, revision rate, CMA accuracy feedback

## Metrics & Events (Event-first design)
- Events (append-only `AnalyticsEvent`)
  - `auth.login_succeeded`, `auth.login_failed`
  - `property.created`, `property.updated`, `property.viewed`
  - `client.created`, `client.updated`, `interaction.logged`
  - `ai.content_generated`, `ai.analysis_completed`, `ai.request_queued`
  - `task.created`, `task.completed`
- Derived metrics (scheduled jobs/materialized views)
  - Content generation count per user/time
  - Conversion funnel by status
  - SLA adherence for AI endpoints
  - Average response time per API route

## Instrumentation Plan
- API middleware captures request metrics and correlation IDs
- Domain services emit events into `AnalyticsEvent`
- Background workers emit processing events (queued/started/completed/failed)

## Dashboards
- Engineering
  - Latency, error rates by endpoint, queue lengths, AI token spend
- Product
  - DAU/WAU, feature adoption, content volume, nurture runs
- Sales/Agent
  - Pipeline metrics, time to first response, CMA cycle time

## Alerts
- Error rate spike > threshold
- p95 latency > SLA for N minutes
- AI spend > budget threshold

## Data Retention
- Raw events retained for 90 days (configurable)
- Aggregates kept indefinitely or per compliance policy
