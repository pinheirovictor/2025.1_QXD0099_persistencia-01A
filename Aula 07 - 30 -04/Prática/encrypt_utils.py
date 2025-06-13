from cryptography.fernet import Fernet
import uuid
import os

async def encrypt_file_symmetric(file):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    content = await file.read()
    encrypted = fernet.encrypt(content)

    output_filename = f"encrypted_{uuid.uuid4().hex}.bin"
    with open(output_filename, "wb") as f:
        f.write(encrypted)

    return {
        "key": key.decode(),  # chave que será usada na decriptação
        "file": output_filename
    }


from cryptography.fernet import Fernet, InvalidToken
import base64
import uuid
import os
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

async def decrypt_file_symmetric(file, key: str):
    try:
        key_bytes = key.encode()
        decoded_key = base64.urlsafe_b64decode(key_bytes)
        if len(decoded_key) != 32:
            return {"error": "Chave inválida: precisa ter 32 bytes base64-safe."}
        fernet = Fernet(key_bytes)
    except Exception as e:
        return {"error": f"Erro na chave: {str(e)}"}

    # Lê o conteúdo criptografado só uma vez
    content = await file.read()

    if not content:
        return {"error": "Arquivo enviado está vazio."}

    try:
        decrypted = fernet.decrypt(content)
    except InvalidToken:
        return {"error": "Chave incorreta ou conteúdo corrompido."}

    output_path = f"decrypted_{uuid.uuid4().hex}.bin"
    with open(output_path, "wb") as f:
        f.write(decrypted)

    return FileResponse(
        output_path,
        filename=os.path.basename(output_path),
        background=BackgroundTask(lambda: os.remove(output_path))
    )
