# honesty.txt — Specification v1

Status: v1
License: MIT (use freely)
Reference implementation: `validator/validate.py` (pure Python, no dependencies)

## 1. Purpose

honesty.txt is a machine-readable declaration of how an application or service handles data. It lets users, auditors and automated agents verify what a service promises versus what it does.

## 2. Placement and format

- Path: `/.well-known/honesty.txt` (RFC 8615)
- Encoding: UTF-8
- Media type: `text/plain`
- Lines starting with `#` are comments
- Sections begin with `## NAME`
- Fields use `key: value` syntax

Known sections: `DATA`, `THIRD-PARTIES`, `TRACKERS`, `PERMISSIONS`, `PROMISES`, `SIGNATURE`. An unknown section produces a warning, not an error.

## 3. Header

All six fields are required (missing field = validation error):

| Field | Meaning |
|---|---|
| `App` | Application identifier (e.g. `com.example.app`) |
| `Host` | Host the declaration applies to |
| `Version` | Declaration / app revision |
| `Contact` | Contact for data inquiries |
| `Updated` | Date of last revision (YYYY-MM-DD) |
| `Expires` | Date after which the declaration is stale (YYYY-MM-DD) |

Date rules: `Updated` and `Expires` must be YYYY-MM-DD (else error); `Expires` must be after `Updated` (else error); a validity period longer than 1 year produces a warning.

## 4. DATA

One line per data type, or `none` if no personal data is collected:

```txt
email: purpose=auth; retain=90d; shared=none
location: purpose=delivery; retain=session; shared=none
photos: purpose=user-content; retain=user-forever; shared=none
```

Format: `field: purpose=...; retain=...; shared=...` — all three keys are required on every line (missing key = validation error).

**purpose** (why):
- `auth` — authentication
- `delivery` — delivery / logistics
- `user-content` — user-generated content
- `analytics` — analytics
- `messaging`, `payment`, `friend-discovery`, `other`

**retain** (how long):
- `session` — only during the session
- `7d`, `30d`, `90d`, `1y`, `2y`, `5y` — days / years
- `none` — not stored
- `user-forever` — until the user deletes
- `forever` — indefinite

**shared** (who receives it):
- `none` — nobody
- a name or domain — the named party only

## 5. THIRD-PARTIES

Names every party referenced in DATA, or `none`:

```txt
payments: stripe.com (card data never touches us)
delivery: cdek.ru (address only)
```

## 6. TRACKERS

`none`, or one tracker identifier per line:

```txt
none
```

```txt
facebook
google-analytics
```

Missing TRACKERS section produces a warning.

## 7. PERMISSIONS

App permissions and their use:

```txt
camera: qr-login
network: core-function
microphone: voice-notes
notifications: message-alerts
```

## 8. PROMISES

Format: `promise: yes|no|details`

```txt
sell-data: no
ad-identifiers: no
delete-on-request: yes-72h
breach-notify: yes-72h
encryption: yes-aes256
```

- `sell-data` — the validator warns if not declared; a verified badge requires `sell-data: no`
- `delete-on-request` — right to erasure, with response time
- `breach-notify` — breach notification commitment
- `encryption` — encryption at rest or end-to-end (e.g. `yes-e2ee`)

## 9. SIGNATURE

Link to the HonestShield certificate:

```txt
badge: HS-2026-000042
```

Before the first audit use `badge: pending-first-audit`. Missing SIGNATURE section produces a warning.

## 10. Validation and statuses

The validator (`validator/validate.py`) produces a report and one of three results:

| Validator result | Badge | Meaning |
|---|---|---|
| `result: OK` | verified | declaration complete and consistent |
| `result: OK (with warnings)` | warnings | valid, but minor issues detected |
| `result: FAIL` | failed | required fields missing or malformed |

Errors fail the check (missing header field, bad dates, DATA line without `purpose`/`retain`/`shared`). Warnings do not fail the check (unknown section, no TRACKERS, no SIGNATURE, validity over 1 year).

Dynamic audit compares the declaration against real behavior; on mismatch the badge is revoked.

## 11. Machine readability

AI agents can parse honesty.txt to make automated decisions:
- allow or refuse interaction
- choose an alternative service
- warn the user

## 12. Regulatory mapping

Each field helps satisfy common regulatory requirements for data handling:

| honesty.txt field | Typical requirement it addresses |
|---|---|
| `purpose` (DATA) | Purpose limitation — data collected only for stated reasons |
| `retain` (DATA) | Storage limitation — data kept only as long as needed |
| `shared` (DATA) + `THIRD-PARTIES` | Third-party disclosure transparency |
| `TRACKERS` | Tracking disclosure and consent |
| `PERMISSIONS` | Permission transparency |
| `sell-data` (PROMISES) | Data sale opt-out / prohibition |
| `delete-on-request` (PROMISES) | Right to erasure |
| `breach-notify` (PROMISES) | Breach notification |
| `Contact` (header) | Designated contact for data inquiries |
| `Updated` / `Expires` (header) | Currency and periodic review |

## 13. Badges

- `assets/badge-verified.svg`
- `assets/badge-warnings.svg`
- `assets/badge-failed.svg`
