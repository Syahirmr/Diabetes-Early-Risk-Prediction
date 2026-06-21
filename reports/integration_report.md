# Integration Report

## 1. cURL /health
```json
{"status":"ok","env":"development","version":"v1"}
```

## 2. Browser Fetch Simulation (Node.js)
```javascript
{ status: 'ok', env: 'development', version: 'v1' }

```

## 3. cURL OPTIONS Preflight
```http
HTTP/1.1 200 OK
date: Sun, 21 Jun 2026 11:16:06 GMT
server: uvicorn
vary: Origin
access-control-allow-methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT
access-control-max-age: 600
access-control-allow-credentials: true
access-control-allow-origin: http://localhost:3000
content-length: 2
content-type: text/plain; charset=utf-8

OK
```

