# Luna Team Operating Charter

## Mission
Run Hidayat Tube website automation as a coordinated team of specialist jobs, with the owner retaining final approval for public release.

## Team

### 1. Luna Coordinator
- Orchestrates the workflow.
- Collects results from specialist checks.
- Stops the release path when a required check fails.

### 2. Website Team
- Inspect HTML/assets/scripts.
- Validate website structure.
- Check automation readiness.
- Prepare deployment report.

### 3. Security Team
- Check for obvious exposed credentials in tracked source.
- Verify the workflow keeps least-privilege permissions.
- Block release if a credential-like pattern is detected.

### 4. Content & YouTube Team
- Prepare Islamic content packages and branding checks.
- Keep YouTube publishing OFF by default.
- Mark content as ready for human review only.

### 5. Reporter Team
- Produce a GitHub Actions summary.
- Report PASS/FAIL/BLOCKED status for each team.
- Record the final approval state.

## Release policy
Draft -> Review -> Approved -> Publish.

Public website deployment and YouTube publishing must not happen automatically without an explicit approval mechanism. API keys belong in GitHub Secrets/environment configuration, never frontend source.

## Operating mode
- Scheduled automation runs daily.
- Push changes can trigger validation.
- Manual dispatch is available for an owner-approved check.
- Failed specialist checks block the release path.
