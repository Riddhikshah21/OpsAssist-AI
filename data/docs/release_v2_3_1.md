# Release Notes v2.3.1

Service: api_gateway  
Source Type: release_notes  
Version: v2.3.1  

## Summary

Release `v2.3.1` introduced API Gateway timeout configuration changes.

## Changes

1. Reduced upstream request timeout from 30 seconds to 10 seconds.
2. Added stricter retry handling for failed upstream requests.
3. Improved logging for upstream timeout errors.
4. Updated default routing rules for Auth Service requests.

## Known Risk

Services with p95 latency above 10 seconds may trigger API Gateway 502 errors.

## Rollback Guidance

If 502 errors increase after this release:

1. Compare error rate with release `v2.3.0`.
2. Check Auth Service latency.
3. Restore upstream timeout to 30 seconds if needed.
4. Escalate to the Platform Team before rollback in production.