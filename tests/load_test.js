import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 20 },
    { duration: '20s', target: 20 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'],
  },
};

export default function () {
  const url = 'http://clickhouse:8123/';
  const query = 'SELECT order_status, count() as orders, sum(total_order_value) as gmv FROM olist.fct_orders GROUP BY order_status';
  
  const res = http.post(url, query, {
    headers: { 
      'Content-Type': 'text/plain',
      'X-ClickHouse-User': 'admin',
      'X-ClickHouse-Key': 'admin123'
    },
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'has data': (r) => r.body && r.body.length > 0,
  });

  if (res.status !== 200) {
    console.log(`Error: ${res.status} ${res.body}`);
  }

  sleep(1);
}
