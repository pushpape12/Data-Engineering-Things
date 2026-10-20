# Docker

Package a reproducible pipeline runtime while keeping configuration and data separate from the image.

[Back to repository index](../README.md)

## Interview revision

Read the [detailed topic explanations, worked examples and interview answers](INTERVIEW.md). Every original topic in this guide is expanded there.

## Prerequisites and lab

Optional Docker Engine lab; build/run not executed here. Dockerfile uses a Python 3.12 image tag for readability, not a locked production digest.

## Topics with worked examples

### Build context and image layers

COPY paths are relative to the build context, not the Dockerfile directory. Build this example from repository root.

```bash
docker build -f docker/Dockerfile -t de-orders:local .
```

**Check:** Creates a standard-library Python image; no cloud credentials or services required.

### Run and inspect

The bundled image runs as a non-root numeric user and processes synthetic data. A fresh disposable container has no persistent output after removal.

```bash
docker run --rm de-orders:local
```

**Check:** Expected stored_orders=3, total_cents=700, rejected_rows=1.

### Persistence and secrets

Mount only dedicated lab output with correct ownership. Pass real credentials using your approved runtime secret system, never a Dockerfile ARG/COPY.

```text
image: application code
volume: durable output
secret store: credentials
environment: non-secret configuration
```

**Check:** For production, pin a verified base-image digest and scan before publishing.

## Official references

- https://docs.docker.com/build/concepts/context/
- https://docs.docker.com/compose/intro/compose-application-model/

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).
