import http from 'k6/http';
import { check, sleep } from 'k6';

const products = JSON.parse(open('../fixtures/products.json'));

export const options = {
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<800'],
  },
};

export default function () {
  const res = http.get(`${__ENV.WEB_URL}/`);
  check(res, {
    'home status is 200': (r) => r.status === 200,
    'home lists every product': (r) =>
      products.names.every((name) => r.body && r.body.includes(name)),
  });
  sleep(1);
}
