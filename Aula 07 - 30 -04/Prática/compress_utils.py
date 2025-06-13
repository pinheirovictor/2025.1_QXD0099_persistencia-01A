import zipfile
import gzip
import tarfile
import os
import uuid
from fastapi.responses import FileResponse


async def compress(file, format: str):
    valid_formats = ["zip", "gzip", "tar.gz", "tar.bz2"]
    if format not in valid_formats:
        return {"error": f"Formato '{format}' não suportado. Use: {', '.join(valid_formats)}"}

    original_filename = file.filename
    unique_id = uuid.uuid4().hex
    temp_input_path = f"temp_{unique_id}_{original_filename}"
    content = await file.read()

    with open(temp_input_path, "wb") as f:
        f.write(content)

    # Definindo nome final do arquivo comprimido
    extension = format.replace('.', '')
    output_path = f"{original_filename}.{extension}"

    try:
        if format == "zip":
            with zipfile.ZipFile(output_path, 'w') as zipf:
                zipf.write(temp_input_path, arcname=original_filename)
        elif format == "gzip":
            with gzip.open(output_path, 'wb') as gz:
                gz.write(content)
        elif format in ["tar.gz", "tar.bz2"]:
            mode = 'w:gz' if format == 'tar.gz' else 'w:bz2'
            with tarfile.open(output_path, mode) as tar:
                tar.add(temp_input_path, arcname=original_filename)
    except Exception as e:
        os.remove(temp_input_path)
        return {"error": f"Erro ao comprimir: {str(e)}"}

    os.remove(temp_input_path)

    # FileResponse será enviado e apagamos o arquivo após envio com background
    return FileResponse(
        path=output_path,
        filename=output_path,
        background=lambda: os.remove(output_path)
    )


async def decompress(file):
    filename = file.filename
    ext = filename.lower().split('.')[-1]
    unique_id = uuid.uuid4().hex
    input_path = f"upload_{unique_id}_{filename}"
    content = await file.read()

    with open(input_path, "wb") as f:
        f.write(content)

    output_dir = f"decompressed_{unique_id}"
    os.makedirs(output_dir, exist_ok=True)

    try:
        if filename.endswith(".zip"):
            with zipfile.ZipFile(input_path, 'r') as zipf:
                zipf.extractall(output_dir)
        elif filename.endswith(".gz") and not filename.endswith(".tar.gz"):
            # Gzip simples, extrai conteúdo direto
            output_file = os.path.join(output_dir, filename[:-3])  # remove .gz
            with gzip.open(input_path, 'rb') as gz_in:
                with open(output_file, 'wb') as f_out:
                    f_out.write(gz_in.read())
        elif filename.endswith(".tar.gz") or filename.endswith(".tar.bz2"):
            mode = "r:gz" if filename.endswith(".tar.gz") else "r:bz2"
            with tarfile.open(input_path, mode) as tar:
                tar.extractall(output_dir)
        else:
            return {"error": f"Formato '{filename}' não suportado para descompressão"}
    except Exception as e:
        return {"error": f"Erro ao descomprimir: {str(e)}"}

    os.remove(input_path)

    # Verifica se só tem 1 arquivo extraído → retorna direto
    arquivos = []
    for root, _, files in os.walk(output_dir):
        for file in files:
            arquivos.append(os.path.join(root, file))

    if len(arquivos) == 1:
        final_file = arquivos[0]
        return FileResponse(
            final_file,
            filename=os.path.basename(final_file),
            background=lambda: os.remove(final_file)
        )
    else:
        # Múltiplos arquivos: zipa todos
        zip_final = f"{output_dir}.zip"
        with zipfile.ZipFile(zip_final, 'w') as zipf:
            for file in arquivos:
                arcname = os.path.relpath(file, output_dir)
                zipf.write(file, arcname=arcname)

        # Limpa extraídos
        for file in arquivos:
            os.remove(file)
        os.rmdir(output_dir)

        return FileResponse(
            zip_final,
            filename="arquivos_extraidos.zip",
            background=lambda: os.remove(zip_final)
        )
