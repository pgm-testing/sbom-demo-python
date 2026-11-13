# PG Atlas D1: Python baseline

This repository tests whether real Python dependencies reach PG Atlas through the existing SBOM Action. It is a demo, not a published package, and must stay unattached to any Atlas project.

## Dependencies

| Q4 project | Dependency | Pin |
| --- | --- | --- |
| Python Stellar SDK | stellar-sdk | 17.0.1 |
| Java Stellar SDK (Python bindings) | stellar-contract-bindings | 0.6.0b0 |
| Stellar Hardware Wallet Support | strledger | 0.11.0 |
| Tansu | tansu | 1.0.1 |
| Well-known control | requests | 2.34.2 |

Source mappings and expected Atlas repository IDs are in `expected.json`. Dependency resolution and an offline smoke check run before the unchanged Action. There is intentionally no precursor dependency-submission action in this baseline.

## Run locally

Install uv 0.9.22, then:

```sh
uv sync --frozen
uv run --frozen python -m unittest -v
uv run --frozen python smoke.py
uv run --frozen python check.py sbom --sbom /path/to/sbom.spdx.json
```

An SBOM check requires the exact package versions and a dependency path from the root repository. Package counts and an HTTP success cannot pass it.

## Run on GitHub

Push to main or manually run **Python SBOM baseline**. Enable GitHub's dependency graph for this repository first. The workflow uses read access and OIDC to submit to https://api.pgatlas.xyz, with the tested Action pinned in the workflow and expected.json.

The workflow records the exported SBOM, checks all five dependencies, locates the submission by matching Atlas’s semantic content hash, and checks processed Atlas repository relationships for the four Stellar probes. requests is asserted in the SBOM; no Atlas project association is required for the control.

The current Action does not expose a submission ID. The correlation check searches up to 50 recent submissions for this repository and matches the semantic hash of the document name, sorted packages and sorted relationships. It ignores volatile export metadata, as Atlas does, so deduplicated submissions can still be identified. An unmatched hash is not treated as success.

Atlas processing can take hours. The baseline polls for up to five minutes; if the worker is still pending, it records `pending-timeout` and `verification_complete: false` without failing solely for the delay. Missing dependency coverage still exits with code 1 and API/processing errors with code 2. Pending is not a verified pass.

Once processing completes, dispatch **Verify processed Atlas submission** with the recorded submission ID, from the same fixture commit used by the baseline. This workflow only reads the API and does not resubmit anything. It verifies submission ownership and that the demo has no project association.

Artifacts are retained for 30 days. Download important baseline evidence into the Phase 1 report before expiry. Artifact metadata contains commit/run references; preserve both the baseline and manual verification links.

## Review

Report actual baseline results, including missing dependencies and delays, before changing workflows to address coverage. Gradle/Swift fixes and other Phase 2 work are tracked in [the D1 plan](https://github.com/SCF-Public-Goods-Maintenance/pg-atlas-sbom-action/issues/10).

## Repository rename

This demo was renamed from `pgm-testing/d1-python` to `pgm-testing/sbom-demo-python`. Submission 2399 and the initial baseline belong to the old repository identity. Preserve that historical evidence; use a new baseline submission for the renamed repository. The verifier intentionally rejects submissions owned by a different repository name.

## Tansu source mapping

PyPI tansu 1.0.1 points to tupui/soroban-versioning. That repository explicitly announces its move to Consulting-Manao/tansu and shares historical release commits with it. The expected Atlas relationship therefore targets the current repository. This is an assertion to test, not a claim that Atlas has already resolved the mapping. The similarly named npm package and Cargo crate are unrelated and excluded.

## Dependency structure check

The baseline also checks that requests depends on urllib3, without treating urllib3 as a direct dependency of this fixture. The previous export flattened all dependencies onto the root. Package-presence results and relationship-structure results are reported separately; a structure failure does not mean the packages were omitted. This captures the limitation without changing the Action or adding a precursor.

## Waiting for Atlas processing

The checker now polls the submission status every 15 seconds for up to five minutes before checking dependency relationships. A processed submission is checked immediately; a processing error or missing relationship still fails.

If the budget expires while the submission is pending, the result is `pending-timeout` with `verification_complete: false`. This keeps the workflow from failing solely because a worker has not run, but it is **not** a verified coverage pass. Run `verify-atlas.yml` with the recorded submission ID later. Its result and the baseline together form the evidence.

Override the polling budget with `--processing-wait-seconds` and `--poll-interval`. Submission-record lookup has its own 90-second budget. API errors remain errors rather than being reported as pending.

Repository settings should stay at their defaults unless a baseline demonstrates a necessary change. Gradle needs automatic dependency submission, enabled by Alex. Do not enable it in the other demos just to match Gradle. Alex owns backend dependency-link corrections; these demos provide evidence and verification.
