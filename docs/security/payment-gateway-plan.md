# South Africa Payout & Cash-Out Plan

Context: Workers are paid in-app by employers; funds must land in a compliant wallet and be withdrawable to a bank account or as cardless ATM cash-out.

## Regulatory Guardrails
- Operate through a licensed payment service provider (PSP) under the National Payment System Act; do not clear/settle directly.
- Apply FIC Act customer due diligence: collect ID, match selfie/ID, verify phone/email, and perform sanctions/PEP screening; risk-rate customers and enforce limits.
- POPIA: minimize data, explicit consent for processing payments/biometrics, provide privacy notice, allow access/erasure; secure cross-border transfers with appropriate safeguards.
- Maintain STR/CTR reporting workflow with the PSP; keep audit trails for at least 5 years.
- Avoid card data handling to stay outside PCI scope; use gateway tokens/hosted fields only.

## Recommended Rails (2026)
- Bank payouts: use an EFT/RTC/PayShap payout API via a PSP with account-name verification and return codes.
- Cardless ATM cash-out: use a PSP that supports voucher-based withdrawals (e.g., Paycorp/ATM Solutions or Ukheshe/Metobank rails) to issue time-bound, PIN-protected vouchers.
- Incoming payments (employers): accept card/instant EFT/PayShap via the same PSP for simplified reconciliation and settlement.

## Shortlisted Providers to Evaluate
- Stitch Payouts: verified bank account payouts with name matching and PayShap support; developer-first API and webhooks.
- Ozow/Floatpays or Paystack (SA) for card + instant EFT; confirm payout support and local licensing status.
- Paycorp/Ukheshe partnership for cardless ATM vouchers.
Choose one PSP that covers payouts + instant EFT/PayShap + voucher cash-out to reduce complexity; confirm licensing and SARB approval in contract.

## Integration Pattern
1) Wallet ledger: maintain an internal ledger per worker/employer. Funds are only moved externally during payout/cash-out. Keep reconciliation-friendly transaction IDs.
2) Onboarding/KYC: collect and verify ID + bank account before first payout; re-verify on bank detail changes. Enforce velocity/value limits by risk tier.
3) Funding: employer pays into PSP (card/PayShap/instant EFT). PSP notifies via webhook; credit employer wallet after confirmation, not on client-side success.
4) Payout to bank: worker requests payout; server authorizes with MFA + velocity checks, creates PSP payout, and records status. Credit completes only on PSP success callback.
5) Cardless ATM: worker chooses cash-out; server requests voucher from PSP, stores masked token, displays retrieval instructions; auto-expire + refund on timeout.
6) Disputes & reversals: build flows for failed payouts, expired vouchers, and chargebacks with audit logs and notifications.

## Security Controls Specific to Payments
- Dual control for high-value or first-time bank accounts; step-up MFA for payout requests and bank detail edits.
- Webhooks: signed, replay-protected, and IP-allowlisted; enqueue idempotent processors.
- Idempotency keys on all payout/cash-out API calls; optimistic locking on ledger writes.
- Reconciliation: daily job comparing PSP reports to ledger; investigate deltas same day.
- Secrets: PSP keys in secret manager; rotate quarterly; separate keys per environment.
- Observability: metrics on payout success rate, reversal rate, fraud flags, voucher expiry, and KYC failures; alerts with runbooks.
- Data retention: purge KYC artifacts after regulatory minimums; mask PAN/token displays.

## Rollout Steps
- Pilot with a small worker/employer cohort; set conservative limits.
- Run pen test focused on payout flows and voucher issuance.
- Conduct tabletop for payout diversion and voucher abuse; refine runbooks.
- Enable staged limits by risk tier; only then widen coverage.
