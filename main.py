from fastapi import FastAPI, Form, UploadFile, File
from fastapi import HTTPException, status

import os
import shutil
from functools import lru_cache
from pathlib import Path
from typing import Any, List, Union, Optional
from whispercpp import Whisper

from datetime import timedelta

app = FastAPI()
w = Whisper('tiny')
UPLOAD_DIR="/tmp"

@app.post('/v1/audio/transcriptions')
async def transcriptions(file: UploadFile = File(...)):
    filename = file.filename
    fileobj = file.file
    upload_name = os.path.join(UPLOAD_DIR, filename)
    upload_file = open(upload_name, 'wb+')
    shutil.copyfileobj(fileobj, upload_file)
    upload_file.close()
    
    result = w.transcribe(upload_name)
    print(result, "result")
    text = w.extract_text(result)
    
    return text