# Internship Watcher

GitHub Actions checks the Simplify 2026/2027 boards and selected company ATS
boards every 15 minutes, then emails newly discovered internships.

## Configuration

Edit `.github/workflow-scripts/watcher_config.json` to control filtering:

- `target_countries`: `US` and/or `CA` (both are enabled by default).
- `keep_ambiguous_locations`: retain listings such as bare `Remote` locations.
- `additional_role_patterns`: regex patterns that include more internship titles.
- `additional_exclude_patterns`: regex patterns that reject titles.

Required Actions secrets are `MAIL_USERNAME`, `MAIL_PASSWORD`, and `MAIL_TO`.
`MAIL_PASSWORD` should be a Gmail App Password.

For external schedule monitoring, create a monitor with a 15-minute expected
period and add its ping URL as the optional `HEARTBEAT_URL` Actions secret. The
workflow reports start, success, and failure. Configure the monitoring service
to alert when pings are late or missing.

Run tests locally with:

```bash
python3 -m unittest discover -s .github/workflow-scripts -p 'test_*.py'
```
