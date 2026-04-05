FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    android-tools-adb \
    python3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY web/ ./web/
COPY entrypoint.sh ./

RUN chmod +x entrypoint.sh

EXPOSE 5555

ENTRYPOINT ["./entrypoint.sh"]
