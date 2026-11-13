# Python Environment Config Checker (`python-env-config-checker`)

A lightweight Python command-line utility for auditing project `.env` configurations, validating required keys against `.env.example` templates, and flagging insecure default credentials.

## Features

- **Template Parity Check:** Identifies missing required environment variables.
- **Security Heuristics:** Flags weak passwords (`password`, `123456`) and short secret keys.
- **Pure Python Standard Library:** Zero external dependencies required.

## Running the Checker

Execute the script from your terminal against a target project folder:

```bash
python3 src/checker.py sample_project
```
