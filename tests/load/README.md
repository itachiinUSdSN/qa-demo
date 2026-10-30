# Load tests (k6)

k6 scripts, one user journey per file: `tests/load/<name>.js`. Scripts read `__ENV.BASE_URL`,
make read-only requests, and set thresholds. They never set the load shape; test.yml does:

- `load` (on demand): light regression gate against staging, 10 virtual users for 1 minute.
- `capacity` (on demand): ramps to 300 virtual users to find the breaking point. Runs only
  against the repo variable `LOAD_CAPACITY_URL`, which must not be staging.

Run with `/test <app> load` or `/test <app> capacity` in Telegram. Never on push.
