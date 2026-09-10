import os
from pathlib import Path
from fastapi import UploadFile


def save_upload_file(upload_file: UploadFile, upload_dir: str = "uploads") -> dict:
    """Save uploaded image to uploads folder and return metadata."""
    Path(upload_dir).mkdir(parents=True, exist_ok=True)

    file_extension = Path(upload_file.filename or "image.jpg").suffix.lower()
    stored_name = f"{Path(upload_file.filename or 'image').stem}_{os.urandom(8).hex()}{file_extension}"
    file_path = Path(upload_dir) / stored_name

    content = upload_file.file.read()
    file_path.write_bytes(content)

    return {
        "filename": upload_file.filename,
        "stored_filename": stored_name,
        "file_path": str(file_path),
        "size": file_path.stat().st_size,
        "content_type": upload_file.content_type,
    }
