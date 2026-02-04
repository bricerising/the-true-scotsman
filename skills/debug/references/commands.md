# Triage Commands (Copy/Paste)

These are intentionally generic templates. Replace placeholders like `<service>`, `<namespace>`, `<route>`, `<method>`, `<traceId>`, `<requestId>`.

## Logs

### Local files (JSON logs)

```sh
rg -n '"level":"error"|\"err\"|timeout|ECONNRESET|ETIMEDOUT|deadline exceeded' -S .
```

Filter JSON logs by `traceId` or `requestId`:

```sh
cat <logfile> | jq -c 'select(.traceId=="<traceId>" or .requestId=="<requestId>")'
```

### Docker Compose

```sh
docker compose logs --since=10m <service>
```

Search within logs:

```sh
docker compose logs --since=10m <service> | rg -n 'error|timeout|traceId|requestId' -S
```

### Kubernetes

```sh
kubectl -n <namespace> get pods -l app=<service>
kubectl -n <namespace> logs deploy/<service> --since=10m
```

Search for a trace/request ID:

```sh
kubectl -n <namespace> logs deploy/<service> --since=30m | rg -n '<traceId>|<requestId>' -S
```

Split by container (if multi-container pod):

```sh
kubectl -n <namespace> logs deploy/<service> -c <container> --since=10m
```

## Traces

### Trace UI (Tempo / Jaeger / vendor APM)

If you have a `traceId`, search for it in your trace UI and inspect:

- slowest span(s)
- first error span(s)
- retries (repeated similar spans)
- deadline/timeout signals (`DEADLINE_EXCEEDED`, `ETIMEDOUT`)

### Tempo HTTP API (optional)

If you have Tempo reachable locally:

```sh
curl -sS "http://<tempo-host>:3200/api/traces/<traceId>" | jq '.'
```

List services involved (heuristic; schema varies by Tempo version):

```sh
curl -sS "http://<tempo-host>:3200/api/traces/<traceId>" \
  | jq -r '.. | objects | .resource?.attributes? // empty | .[]? | select(.key=="service.name") | .value?.stringValue' \
  | sort -u
```

## Metrics (Prometheus-compatible)

### Quick “is it on fire?” check

```sh
curl -sS -G "http://<prom-host>:9090/api/v1/query" \
  --data-urlencode 'query=up{job="<service>"}'
```

### HTTP RED (examples)

Request rate:

```sh
curl -sS -G "http://<prom-host>:9090/api/v1/query" \
  --data-urlencode 'query=sum(rate(http_server_requests_total{service="<service>"}[5m]))'
```

Error rate:

```sh
curl -sS -G "http://<prom-host>:9090/api/v1/query" \
  --data-urlencode 'query=sum(rate(http_server_requests_total{service="<service>",status=~"5.."}[5m]))'
```

p95 latency (histogram):

```sh
curl -sS -G "http://<prom-host>:9090/api/v1/query" \
  --data-urlencode 'query=histogram_quantile(0.95, sum by (le) (rate(http_server_request_duration_seconds_bucket{service="<service>"}[5m])))'
```

### gRPC RED (examples)

RPC rate and errors:

```sh
curl -sS -G "http://<prom-host>:9090/api/v1/query" \
  --data-urlencode 'query=sum(rate(grpc_server_handled_total{grpc_service="<Service>",grpc_method="<Method>"}[5m]))'
```

```sh
curl -sS -G "http://<prom-host>:9090/api/v1/query" \
  --data-urlencode 'query=sum(rate(grpc_server_handled_total{grpc_service="<Service>",grpc_method="<Method>",grpc_code!="OK"}[5m]))'
```

### Saturation / resource hints (examples)

Pod CPU/memory (k8s metrics-server required):

```sh
kubectl -n <namespace> top pods -l app=<service>
```

Node.js event loop lag (if exported):

```sh
curl -sS -G "http://<prom-host>:9090/api/v1/query" \
  --data-urlencode 'query=max(nodejs_eventloop_lag_p99_seconds{service="<service>"})'
```

## Repro / boundary checks

### HTTP

```sh
curl -v --max-time 10 "http://<host>:<port><route>"
```

### gRPC (grpcurl)

List services:

```sh
grpcurl -plaintext <host>:<port> list
```

Call a method:

```sh
grpcurl -plaintext -d '{}' <host>:<port> <package.Service>/<Method>
```

### Async consumers (common hints)

These depend on your queue/broker. Examples:

- Redis Streams:
  - `redis-cli XLEN <stream>`
  - `redis-cli XINFO GROUPS <stream>`
- Kafka:
  - `kafka-consumer-groups --bootstrap-server <broker> --describe --group <group>`

