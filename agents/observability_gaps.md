# Agent: Observability Gaps

A structured QA workflow for identifying missing or insufficient observability coverage
in a system — metrics, logs, traces, and alerts — before those gaps surface as invisible
production failures.

## Purpose

Observability gaps are a force-multiplier for defects: a bug in a well-instrumented
system is found in minutes; the same bug in an unobservable system can go undetected for
days or weeks. This workflow surfaces gaps systematically so they can be closed alongside
feature work, not as a post-incident afterthought.

## Inputs

| Input | Description |
|-------|-------------|
| `architecture_diagram` | Service/component map (diagram or YAML) |
| `runbook_inventory` | List of existing runbooks and on-call playbooks |
| `alert_definitions` | Current alerting rules (e.g. Prometheus, Datadog, PagerDuty) |
| `log_schema` | Structured log field catalogue (optional) |
| `slo_definitions` | Service-level objectives for each user-facing operation |

## Workflow Steps

### Step 1 – Map critical user journeys

Identify the top user journeys that generate business value or carry the highest user
impact if degraded:

```yaml
journeys:
  - id: CUJ-001
    name: "User completes a purchase"
    services: [frontend, cart-service, payment-service, order-service, notification-service]
  - id: CUJ-002
    name: "User resets password"
    services: [frontend, auth-service, email-service]
```

### Step 2 – Instrument each service hop

For every service involved in a critical user journey, verify the presence of:

| Signal | Required Instrumentation |
|--------|--------------------------|
| **Metrics** | Request rate, error rate, latency (p50/p95/p99) |
| **Logs** | Structured logs with `trace_id`, `user_id` (or pseudonym), outcome |
| **Traces** | Distributed trace span covering the full operation |
| **Alerts** | Error budget burn alert tied to SLO |

```
FOR EACH service IN journey.services:
  FOR EACH required_signal IN [metrics, logs, traces, alerts]:
    IF signal NOT present OR incomplete:
      flag as GAP{service, signal, journey_id, severity}
```

### Step 3 – Classify gap severity

| Severity | Criteria |
|----------|----------|
| CRITICAL | Gap hides a complete service outage |
| HIGH | Gap delays incident detection by > 5 minutes |
| MEDIUM | Gap prevents root-cause identification without manual investigation |
| LOW | Gap reduces diagnostic efficiency but does not affect MTTR materially |

### Step 4 – Validate alert coverage

For each SLO, verify:

1. A burn-rate alert exists at the fast-burn threshold (e.g. 2 % budget in 1 h)
2. A burn-rate alert exists at the slow-burn threshold (e.g. 5 % budget in 6 h)
3. Alert routes to the correct on-call rotation
4. A corresponding runbook exists and was updated within the last 90 days

```
FOR EACH slo IN slo_definitions:
  check fast_burn_alert, slow_burn_alert, routing, runbook_freshness
  IF any check fails:
    flag as ALERT_GAP{slo_id, missing_element}
```

### Step 5 – Synthetic coverage check

For each critical user journey, verify that a synthetic monitor or canary test exists:

- Runs at ≥ 1 min intervals in production (or staging as a minimum)
- Asserts on the observable outcome (status, latency, payload correctness)
- Failure triggers the on-call alert within 2 minutes

### Step 6 – Produce gap report

```yaml
observability_gaps:
  - id: OG-001
    service: payment-service
    signal: traces
    journey: CUJ-001
    severity: CRITICAL
    description: "No distributed trace spans emitted for /charge endpoint"
    remediation: "Instrument with OpenTelemetry SDK; propagate W3C trace context"
    owner: payments-team

  - id: OG-002
    service: notification-service
    signal: alerts
    journey: CUJ-001
    severity: HIGH
    description: "No SLO burn-rate alert for email delivery latency"
    remediation: "Define latency SLO; add Prometheus alerting rule"
    owner: platform-team
```

## Outputs

```
observability_gap_report.yaml   # Machine-readable gap list with owners
observability_summary.md        # Narrative summary for engineering review
gap_remediation_tickets.md      # Pre-filled ticket templates for each gap
```

## Integration Points

- Run after [Risk Analysis](./risk_analysis.md) — focus on CRITICAL/HIGH risk components first
- Attach `observability_gap_report.yaml` to the release checklist
- Use `gap_remediation_tickets.md` to file work in the backlog before the release ships

## Heuristics and Anti-Patterns

### Common gaps to look for

- Services that only emit `INFO` logs on the happy path — errors are silent
- Async workers with no dead-letter-queue monitoring
- Database queries with no slow-query threshold alert
- Third-party integrations with no timeout or circuit-breaker metric
- Front-end errors collected client-side but never correlated with back-end traces

### Anti-patterns to call out

| Anti-Pattern | Risk |
|--------------|------|
| Logging inside catch-blocks only | Happy-path failures invisible |
| Alert thresholds set to `0` errors | Alert fatigue → ignored alerts |
| Trace sampling at 0.1 % | P99 latency anomalies never captured |
| Runbooks that say "check the dashboard" | No actionable remediation steps |
