# Security Readiness Checklist

Use this checklist before every major release and after significant infrastructure or payment changes. Mark each item as done, n/a, or blocked with a short note and ticket link.

## Governance & Risk
- [ ] Threat model updated for web, mobile, backend, and payment flows; high-risk abuse cases captured (fraud, payout diversion, SIM swap, ATM misuse).
- [ ] Data classification applied to all assets; POPIA lawful basis documented for each personal-data use.
- [ ] Incident response playbooks tested (tabletop) with on-call rotations and paging verified.
- [ ] Backups encrypted, tested restores, and RPO/RTO meet business targets.

## Identity & Access
- [ ] SSO + MFA enforced for admin/staff tools; least-privilege roles reviewed quarterly.
- [ ] API auth uses short-lived tokens (JWT/opaque) with audience/issuer checks; refresh rotation enabled.
- [ ] Rate limiting, IP/device fingerprinting, and anomaly detection on login, payouts, and bank detail changes.
- [ ] Session management: HTTP-only + Secure cookies, SameSite=Lax/Strict, and idle/absolute timeouts.

## Application Security
- [ ] Input validation and output encoding cover OWASP Top 10; centralized validation layer present.
- [ ] CSRF protection enabled for state-changing requests; CSP, HSTS, X-Content-Type-Options, X-Frame-Options set.
- [ ] File upload constraints (type/size/AV scan/storage isolation) enforced.
- [ ] Dependency scanning (SCA) and SAST run in CI; critical issues blocked; SBOM produced per release.
- [ ] DAST against staging (authenticated) before release; fixes tracked.
- [ ] Secrets never in repo; stored in a secret manager with rotation policy and audit trails.

## Platform & Network
- [ ] TLS 1.2+ everywhere; modern ciphers; cert automation (ACME) in place.
- [ ] Service-to-service auth (mTLS or workload identity) enabled; no plaintext intra-cluster traffic.
- [ ] Principle of least privilege on cloud/IaC roles; prod separated from non-prod; admin access bastioned and logged.
- [ ] Containers/images are signed, scanned, and pulled with pinning; base images patched monthly.
- [ ] Centralized logging with immutable storage; SIEM rules for auth anomalies, payout changes, and privilege escalations.

## Data Protection
- [ ] Encryption at rest (DB, object storage, backups) with separate KMS; key rotation policy defined.
- [ ] Data minimization: only required personal/bank data collected; retention + deletion jobs implemented.
- [ ] POPIA data subject rights flows tested (access/rectify/delete/consent withdrawal).

## Payment & Payout Safety
- [ ] PCI DSS scope minimized: no PAN storage; card data tokenized via gateway SDK/API only.
- [ ] Bank account verification (account-holder match) required before first payout and on bank detail changes.
- [ ] Payout authorization uses step-up MFA and dual control for high-value/velocity anomalies.
- [ ] Reconciliation jobs verify gateway reports vs. internal ledger daily; dispute/chargeback workflow defined.
- [ ] Fraud controls: device binding for workers, geovelocity checks, and watchlists for mule behavior.
- [ ] Audit logs immutable for all payout events (who/what/when/source IP/device).

## Mobile (Worker/Employer Apps)
- [ ] Root/jailbreak detection, debugger detection, and screenshot protection on sensitive screens.
- [ ] Secure storage (Keystore/Keychain) for tokens; no secrets in app bundle; code obfuscation enabled.
- [ ] Certificate pinning for API hosts; graceful pin rotation path.

## Observability & Testing
- [ ] Synthetic monitors for auth and payout flows; alerts with actionable runbooks.
- [ ] Pen test covering web, mobile, APIs, and payment integrations at least annually; findings tracked to closure.
- [ ] Chaos/fire-drill for key compromise and payout diversion scenarios.

## Compliance (South Africa)
- [ ] NPS Act alignment: use a licensed payment service provider for clearing/settlement.
- [ ] FIC Act obligations: KYC/beneficial-owner checks, sanctions screening, STR/CTR reporting procedure.
- [ ] POPIA/CPA notices and consent records present in app flows; privacy policy matches data processing.

