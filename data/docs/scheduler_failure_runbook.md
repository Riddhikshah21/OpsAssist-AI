# Scheduler Failure Runbook

Service: scheduler  
Source Type: runbook  
Version: v1.0  

## Problem

The Scheduler Service fails to start jobs or retries jobs repeatedly.

## Common Causes

1. Queue backlog
2. Worker process failure
3. Database lock contention
4. Invalid job configuration
5. Auth token validation failure

## Troubleshooting Steps

1. Check scheduler logs for `job_retry_limit_exceeded`.
2. Verify worker health.
3. Check queue depth.
4. Confirm Auth Service is responding normally.
5. Escalate to the Scheduler Team if failures affect critical workflows.

## Related Services

- Auth Service
- Monitoring Service
- Data Ingestion Service