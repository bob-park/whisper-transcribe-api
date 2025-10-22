FROM linuxserver/faster-whisper AS base

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 최종 이미지
FROM base

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY main.py .

EXPOSE 8080

CMD ["python", "main.py"]