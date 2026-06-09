# Auth Service Latency Guide

Service: auth_service  
Source Type: troubleshooting_guide  
Version: v1.0  

## Problem

High Auth Service latency can cause dependent services to fail or timeout.

## Symptoms

- Increased login response time
- Token validation delays
- API Gateway 502 errors
- Repeated `upstream_timeout` messages in gateway logs

## Common Causes

1. Database connection pool exhaustion
2. Slow token validation
3. Increased authentication traffic
4. Deployment regression
5. Cache miss spikes

## Troubleshooting Steps

1. Check Auth Service p95 and p99 latency.
2. Inspect token validation error logs.
3. Review recent deployments.
4. Check database connection pool usage.
5. Roll back the latest Auth Service deployment if latency remains elevated.

## Related Services

- API Gateway
- Dashboard UI
- Scheduler Service