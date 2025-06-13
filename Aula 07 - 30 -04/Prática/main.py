from fastapi import FastAPI, UploadFile, File, Form
import compress_utils, encrypt_utils, hash_utils
from fastapi import UploadFile, File

app = FastAPI()

@app.post("/Compressao/")
async def compress_file(file: UploadFile = File(...), format: str = Form(...)):
    return await compress_utils.compress(file, format)

@app.post("/descompressao/")
async def decompress_file(file: UploadFile = File(...)):
    return await compress_utils.decompress(file)


@app.post("/encrypt/")
async def encrypt_file(file: UploadFile = File(...)):
    return await encrypt_utils.encrypt_file_symmetric(file)

@app.post("/decrypt/")
async def decrypt_file(file: UploadFile = File(...), key: str = Form(...)):
    return await encrypt_utils.decrypt_file_symmetric(file, key)

@app.post("/hash/")
async def hash_file(file: UploadFile = File(...), algorithm: str = Form(...)):
    return await hash_utils.generate_hash(file, algorithm)

