# Mobile tests (Maestro)

Maestro YAML flows, one behaviour per file: `tests/mobile/<name>.yaml`.
They run on an Android emulator in CI against the staging build at the repo
variable `STAGING_APK_URL`. Without that variable the mobile suite is skipped.
Put the app id at the top of each flow (`appId: com.example.app`); test data comes from tests/fixtures.
