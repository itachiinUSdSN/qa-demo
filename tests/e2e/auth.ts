// Signed-in browser tests:
//   test.skip(!hasRole('sales'), 'no staging QA user for sales');
//   test.use({ storageState: asRole('sales') });
// Uses the token the CI sign-in step saved for that staging QA user (QA_TOKENS); the app keeps
// its sign-in token in localStorage "token". Skips cleanly when there is no token.
import fs from 'fs';
import os from 'os';
import path from 'path';

export function hasRole(role: string): boolean {
  const file = process.env.QA_TOKENS;
  return !!file && fs.existsSync(file) && role in JSON.parse(fs.readFileSync(file, 'utf8'));
}

export function asRole(role: string): string {
  const out = path.join(os.tmpdir(), `qa-state-${role}.json`);
  if (!hasRole(role)) {
    fs.writeFileSync(out, JSON.stringify({ cookies: [], origins: [] }));
    return out;
  }
  const token = JSON.parse(fs.readFileSync(process.env.QA_TOKENS!, 'utf8'))[role].token;
  const origin = new URL(process.env.STAGING_URL!).origin;
  fs.writeFileSync(out, JSON.stringify({ cookies: [], origins: [{ origin, localStorage: [{ name: 'token', value: token }] }] }), { mode: 0o600 });
  return out;
}
