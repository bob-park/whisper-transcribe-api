# Whisper transcribe API
이것은 오디오 파일을 `fast whisper` 를 이용해서 Speech To Text 로 변환해주는 api 이다.

## Docker 실행
```bash
docker run -it -d \
  --name=whisper-trasncribe-api \
  -p 5002:8000 \
  ghcr.io/bob-park/whisper-transcribe-api
```