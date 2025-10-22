from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile
import torch
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
    if torch.cuda.is_available():
        logger.debug("CUDA device detected")
        return WhisperModel('large-v3', device="cuda", compute_type="float16")
    else:
        logger.debug("Using CPU device")
        return WhisperModel('base', device="cpu", compute_type="int8")


model = get_models()


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
