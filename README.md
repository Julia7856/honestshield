[![validate-examples](https://github.com/Julia7856/honestshield/actions/workflows/validate.yml/badge.svg)](https://github.com/Julia7856/honestshield/actions/workflows/validate.yml)

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

## Adopt it in 5 minutes

### Step 1. Create honesty.txt

Copy the [example](examples/shop.honesty.txt) and fill in your data. Required:
- header (App, Host, Contact, dates)
- DATA section (what data and why)
- PROMISES section (`sell-data: no` is mandatory)

### Step 2. Place it at

```
https://your-site.com/.well-known/honesty.txt
```

This is [RFC 8615](https://www.rfc-editor.org/rfc/rfc8615) — the standard location for site metadata.

### Step 3. Run the validator

Locally:
```bash
python validator/validate.py honesty.txt
```

Or via URL:
```bash
python validator/validate.py --url https://your-site.com
```

You should see `result: OK` (warnings are fine).

### Step 4. Link it in your footer

```html
<footer>
  <a href="/.well-known/honesty.txt">honesty.txt</a>
</footer>
```

### Step 5 (optional). Add a badge

Once the certification system launches, we'll add a green "honesty.txt verified" badge.

## The standard

See [STANDARD.md](STANDARD.md) — the full honesty.txt specification.

## Validator

Reference implementation — `validator/validate.py` (pure Python, no dependencies):

```bash
python validator/validate.py examples/shop.honesty.txt
python validator/validate.py --url https://example.com
```

GitHub Actions runs the check on every commit — the badge above is live proof.

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
