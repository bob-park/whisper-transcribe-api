from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile
from faster_whisper import WhisperModel
import uvicorn
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()


def get_models():
    model_size = os.environ.get("MODEL_SIZE") or 'small'
    compute_type = os.environ.get("COMPUTE_TYPE") or 'int8'
    model_path = os.environ.get("MODEL_PATH") or './models'

    absolute_download_path = f"{model_path}/{model_size}"

    logger.debug(f"Loading model {model_size} with compute type {compute_type}")
    logger.debug(f"Downloading model to {absolute_download_path}")

    return WhisperModel(
        model_size_or_path=model_size,
        device="cpu",
        compute_type=compute_type,
        download_root=absolute_download_path)


model = get_models()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        audio_path = tmp.name
        content = await file.read()
        tmp.write(content)

    segments, info = model.transcribe(audio_path, beam_size=5)

    results = []
    for segment in segments:
        results.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })

    info_dict = {
        "language": info.language,
        "duration": info.duration,
    }

    os.remove(audio_path)

    return JSONResponse(content={"segments": results, "info": info_dict})
