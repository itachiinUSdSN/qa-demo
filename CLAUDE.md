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
- Tests run against STAGING_URL only. Never a production URL, never real customer data.
<!-- qa-agents:end -->
