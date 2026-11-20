# CLAUDE.md — Weather-Station

## Purpose

New weather-station project (currently empty). Likely shares hardware and patterns with
`SMART---GREENHOUSE` (ESP32, I²C sensors, batch upload to a backend) — reuse its approach where it fits,
but confirm with the owner before assuming the hardware.

## Suggested structure

```
firmware/     # microcontroller code
backend/      # API / database
dashboard/    # visualisation
docs/         # wiring diagrams, photos
```

## Conventions

- Keep the README sections filled as code lands: Features, Hardware (sensor table with pins),
  Getting started, Data format.
- Never commit Wi-Fi credentials or API keys — use a git-ignored `secrets.h` / `.env`.
- Commit messages: imperative, short (`Add BME280 driver`, `Fix upload retry`).

## Do not

- Do not invent features in the README — mark unknowns as TODO.
