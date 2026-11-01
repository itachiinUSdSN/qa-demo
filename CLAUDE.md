<!-- qa-agents:start -->
# Testing rules (qa-agents)

- Goal first: state the success check before writing code.
- Never change an assertion to make a test pass; if behaviour changed, say so in the PR.
- Healer mode: edit only locators and waits in the failing test file.
- Locators: getByRole / getByLabel / data-testid. No CSS chains, no XPath. No sleeps.
- Declare a locator in a const before the expect that uses it, so a locator fix never touches an assertion line.
- Test data from tests/fixtures only. Locators and test ids stay in the test file, never in fixtures.
- One test = one behaviour. No helpers until the third copy.
- Done = runner output shows green; paste the summary in the PR.
- Tests run against STAGING_URL (and STAGING_API_URL for the API) only. Never a production URL, never real customer data.
- Signed-in tests use the staging QA users only: `signed_in("<role>")` (API) or `asRole('<role>')` (browser). Pick the least-privileged role that can do the job; `owner` only for owner-only screens. Never type or store a password.
- Every record a test creates has a name or title starting with `QA-TEST` (fixtures too). A nightly job deletes them. Never edit or delete a record the test did not create.
- No payments, real emails or messages to real people, even on staging.
<!-- qa-agents:end -->
