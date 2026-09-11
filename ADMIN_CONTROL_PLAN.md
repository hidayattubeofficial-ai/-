# Hidayat Tube Official — Admin & Luna Control

## Ownership
- Website operations: Luna/automation layer
- YouTube operations: Luna assistant oversight
- Project owner: Hidayat Tube Official

## Control model
1. Luna may inspect, validate, prepare, test, and report website changes.
2. Luna may run approved automation workflows.
3. Public website deployment requires an explicit approval signal.
4. YouTube publishing remains disabled until human approval.
5. API keys and tokens must never be placed in frontend code.
6. Every important automation run must leave an auditable GitHub Actions summary.

## Planned admin controls
- Website health/status
- Content queue: Draft → Review → Approved → Published
- Automation workflow status
- Deployment approval
- YouTube publishing ON/OFF gate
- Error/security reports
- Messenger/Luna command status
- Audit log

## Safety boundary
The control layer must not bypass human approval for public release, expose credentials, or silently change publishing permissions.
