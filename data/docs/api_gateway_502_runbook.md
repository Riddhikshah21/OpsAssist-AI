# API Gateway 502 Runbook

Service: api_gateway  
Source Type: runbook  
Version: v1.0  

## Problem

The API Gateway returns HTTP 502 errors when it cannot receive a valid response from an upstream service.

## Common Causes

1. Upstream service timeout
2. Auth Service latency
3. Incorrect gateway timeout configuration
4. Failed deployment or incompatible service version
5. Network connectivity issues between services

## Troubleshooting Steps

1. Check recent API Gateway logs for `upstream_timeout` or `bad_gateway`.
2. Check Auth Service latency and error rate.
3. Verify whether a recent release changed timeout settings.
4. Compare the current gateway version with the previous stable release.
5. Escalate to the Platform Team if errors continue for more than 15 minutes.

## Recommended Action

If 502 errors started after release `v2.3.1`, verify the upstream timeout configuration and check Auth Service latency.