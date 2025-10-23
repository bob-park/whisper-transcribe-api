# Whisper transcribe API

이것은 오디오 파일을 `fast whisper` 를 이용해서 Speech To Text 로 변환해주는 api 이다.

## Model

### models

| 모델 이름      | 파라미터 수 | 파일 크기 (대략) | 정확도   | 속도    | 메모리 사용 | 권장 환경              |
|------------|--------|------------|-------|-------|--------|--------------------|
| `tiny`     | ~39M   | 75 MB      | 낮음    | 매우 빠름 | 매우 적음  | 저사양 CPU, 테스트       |
| `base`     | ~74M   | 142 MB     | 보통    | 빠름    | 적음     | 기본 데모, 경량 환경       |
| `small`    | ~244M  | 466 MB     | 좋음    | 보통    | 중간     | CPU/GPU 겸용, 밸런스형   |
| `medium`   | ~769M  | 1.5 GB     | 매우 좋음 | 느림    | 많음     | GPU 권장, 배치 변환      |
| `large-v1` | ~1.55B | 3.1 GB     | 최고    | 매우 느림 | 매우 많음  | 고정밀 변환, 방송급        |
| `large-v2` | ~1.55B | 3.1 GB     | 최고+   | 매우 느림 | 매우 많음  | 최신 추천 버전           |
| `large-v3` | ~1.55B | 3.1 GB     | 최고++  | 매우 느림 | 매우 많음  | Whisper 최신 성능 (추천) |

### compute types

| compute_type   | 설명                     | 연산 속도 | VRAM/메모리 사용 | 정확도   | 권장 환경           |
|----------------|------------------------|-------|-------------|-------|-----------------|
| `float32`      | 기본 32비트 부동소수점          | 느림    | 높음          | 최고    | CPU 또는 정밀도 테스트  |
| `float16`      | 16비트 부동소수점             | 빠름    | 중간          | 거의 동일 | GPU (FP16 지원 시) |
| `int8`         | 8비트 정수 양자화             | 빠름    | 낮음          | 약간 하락 | CPU (속도 향상용)    |
| `int8_float16` | 가중치는 int8, 계산은 float16 | 빠름    | 낮음          | 미세 손실 | GPU 최적형         |
| `int16`        | 16비트 정수                | 중간    | 중간          | 거의 동일 | 일부 CPU 환경용      |

## Build & Deploy

### Docker 실행

```bash
docker run -it -d \
  --name=whisper-trasncribe-api \
  -p 5002:8000 \
  ghcr.io/bob-park/whisper-transcribe-api
```

### Docker Compose

```yaml
services:
  whisper-transcribe-api:
    image: ghcr.io/bob-park/whisper-transcribe-api
    ports:
      - 8000:8000
    environment:
      - MODEL_SIZE=small # optional
      - COMPUTE_TYPE=int8 # optional
      - MODEL_PATH=/app/models # optional
    volumes:
      - "./models:/app/models"
```