# Docker: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. Build context and image layers
2. Run and inspect
3. Persistence and secrets

## 1. Build context and image layers

### Understand it

Docker COPY paths resolve against build context. Layers can improve rebuild reuse, but sensitive files copied in an earlier layer may remain recoverable even if deleted later. Keep context narrow and use .dockerignore when broad contexts could include secrets.

### Practical example

```bash
docker build -f docker/Dockerfile -t de-orders:local .
```

**Expected result and reasoning:** Run at repository root so python/etl.py and datasets/ are in context. The supplied Dockerfile copies only those needed inputs.

### Interview question

**Why does COPY fail when the file exists?**

The path may be outside context, excluded, differently cased or referenced relative to the wrong directory. Check the build command, not just the Dockerfile location.

**Common mistake:** COPY . . with a broad context that may contain credentials or local databases.

**Try it yourself:** Design a .dockerignore for a production data service.

## 2. Run and inspect

### Understand it

An image is a packaged template; a container is a running instance. Process exit status and logs support job diagnosis. The bundled job runs as a non-root user and only processes synthetic local data.

### Practical example

```bash
docker run --rm de-orders:local
```

**Expected result and reasoning:** On a successful optional build/run, logs report three stored orders, 700 cents and one reject. --rm removes the container after exit.

### Interview question

**Why does output disappear after a container exits?**

Files written to its ephemeral filesystem are not a durable data product. Publish to an authorized object store/database or mount a properly permissioned dedicated volume when persistence is required.

**Common mistake:** Treating a successful container exit as proof an external dataset was published correctly.

**Try it yourself:** Explain how an orchestrator would detect job failure and safely retry.

## 3. Persistence and secrets

### Understand it

Externalize durable state and runtime credentials. A volume needs correct ownership/access; a secret needs controlled injection rather than source/image embedding. Mutable image tags are convenient for learning but insufficient release identity.

### Practical example

```text
release: verified image digest
runtime identity: non-root user
state: dedicated storage or database
credentials: approved secret mechanism
```

**Expected result and reasoning:** A reproducible release can identify exactly which image ran, and a rebuilt image need not contain credentials.

### Interview question

**How would you secure this image for deployment?**

Pin a verified base digest, scan dependencies/image, use least privilege, minimize filesystem writes and inject secrets at runtime. Verify mounted output permissions for the selected UID.

**Common mistake:** Putting tokens in Dockerfile ARG/ENV and assuming they are invisible.

**Try it yourself:** Describe rotating a database credential without rebuilding the application.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.
