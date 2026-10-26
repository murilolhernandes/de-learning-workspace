# Local Spark + Delta environment for the crash course. No cloud, no credentials.
FROM python:3.12-slim-bookworm

# Spark 3.5 needs a JVM. Java 17 is one of its supported versions.
RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-17-jre-headless procps \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workspace

# Install pinned dependencies first so Docker caches this layer.
COPY requirements.txt .
RUN pip install -r requirements.txt

# The project itself is bind-mounted at run time, so edits show up without a rebuild.
# Delta jars are downloaded once into /root/.ivy2 (mount a volume there to keep them).
CMD ["pytest"]
