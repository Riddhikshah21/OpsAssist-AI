# Engineering Escalation Policy

Service: platform  
Source Type: policy  
Version: v1.0  

## When to Escalate

Escalate an incident when:

1. The issue impacts multiple users.
2. The issue lasts longer than 15 minutes.
3. The assistant has low confidence.
4. The system detects repeated production errors.
5. The issue involves authentication, data loss, or service availability.

## Escalation Information Required

Include the following in every escalation summary:

1. Affected service
2. User-visible symptoms
3. Relevant logs or error messages
4. Recent release or configuration changes
5. Troubleshooting steps already attempted
6. Recommended owning team

## Owning Teams

- API Gateway issues: Platform Team
- Auth Service issues: Identity Team
- Scheduler issues: Workflow Team
- Monitoring issues: Observability Team