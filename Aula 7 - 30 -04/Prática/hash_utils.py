import hashlib

async def generate_hash(file, algorithm):
    content = await file.read()
    if algorithm == "md5":
        hash_val = hashlib.md5(content).hexdigest()
    elif algorithm == "sha1":
        hash_val = hashlib.sha1(content).hexdigest()
    elif algorithm == "sha256":
        hash_val = hashlib.sha256(content).hexdigest()
    else:
        return {"error": "Algoritmo inválido"}
    
    return {"algorithm": algorithm, "hash": hash_val}
