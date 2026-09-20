[![validate-examples](https://github.com/Julia7856/honestshield/workflows/validate-examples/badge.svg)](https://github.com/Julia7856/honestshield/actions)

**English** | [Русский](README.ru.md)

# HonestShield

A certificate of honesty for applications.

Like Energy Star for refrigerators, but for data practices. An app publishes `honesty.txt` — a machine-readable declaration of how it handles data. HonestShield verifies real behavior against the declaration. Match → green badge. Lie → red.

## The problem

Data policies are 40 pages of text nobody reads. Developers promise one thing and do another. Users don't know whom to trust.

## The solution

HonestShield makes data handling **transparent**:
- Machines read honesty.txt in a second
- Users see an honesty badge
- Developers face market pressure (no badge = no trust)

## How it works

1. A service publishes `/.well-known/honesty.txt`
2. HonestShield parses the declaration
3. A dynamic audit checks real traffic
4. Cross-check: declaration vs. behavior
5. Issue or revoke the certificate
6. A daily bot re-checks every registered service — results are public

## Live tools

- **Web validator**: https://julia7856.github.io/honestshield/ — check any declaration in the browser, share a report link, copy a badge snippet
- **Registry status**: https://julia7856.github.io/honestshield/status.html — who is honest today, updated daily by GitHub Actions

## Adopt it in 5 minutes

### Step 1. Create honesty.txt

Copy the example and fill in your data. Required:
- header (App, Host, Contact, dates)
- DATA section (what data and why)
- PROMISES section (`sell-data: no` is mandatory)

### Step 2. Place it atThis is RFC 8615 — the standard location for site metadata.

### Step 3. Run the validator

Locally:
```bash
python validator/validate.py honesty.txt
```

Or via URL:
```bash
python validator/validate.py --url https://your-site.com
```

Or in the browser: [web validator](https://julia7856.github.io/honestshield/).

You should see `result: OK` (warnings are fine).

### Step 4. Link it in your footer

```html
<footer>
  <a href="/.well-known/honesty.txt">honesty.txt</a>
</footer>
```

### Step 5 (optional). Add a badge

The badges already exist — copy the ready-made snippet from the web validator (it picks the exact badge for your result), or use:

```html
<img src="https://raw.githubusercontent.com/Julia7856/honestshield/main/assets/badge-verified.svg" alt="honesty.txt: verified" height="20">
```

## The standard

See STANDARD.md — the full honesty.txt specification.

## Validator

Reference implementation — `validator/validate.py` (pure Python, no dependencies):

```bash
python validator/validate.py examples/shop.honesty.txt
python validator/validate.py --url https://example.com
```

GitHub Actions runs the check on every commit — the badge above is live proof.

## Badges

Three states of verification:

![verified](assets/badge-verified.svg) — declaration fully matches behavior.
![warnings](assets/badge-warnings.svg) — declaration is valid, but minor issues detected.
![failed](assets/badge-failed.svg) — declaration does not match behavior.

To place a badge on your site, use:

```html
<img src="https://raw.githubusercontent.com/Julia7856/honestshield/main/assets/badge-verified.svg" alt="honesty.txt: verified" height="20">
```

## Example honesty.txt

```txt
# HONESTY.TXT — v1
App: com.example.app
Host: example.com
Version: 42
Contact: data@example.com
Updated: 2026-09-02
Expires: 2027-03-02

## DATA
email: purpose=auth; retain=90d; shared=none
location: purpose=delivery; retain=session; shared=none

## TRACKERS
none

## PROMISES
sell-data: no
delete-on-request: yes-72h
```

## License

MIT — use freely.

---

**An honesty badge that cannot be faked.**
