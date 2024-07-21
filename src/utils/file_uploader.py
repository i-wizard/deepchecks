from fastapi import UploadFile
import aiofiles


async def stream_file_upload(file: UploadFile) -> str:
    """
    This function will stream a file upload instead of loading the entire file in memory
    thus making large file upload more memory efficient.
    Args:
        file (UploadFile): The file to be uploaded.

    Returns:
        str: The path to the temporary uploaded file.
    """
    temp_file = f"/tmp/{file.filename}"
    async with aiofiles.open(temp_file, 'wb') as out_file:
        # Adjust chunk size as necessary
        while content := await file.read(1024):
            await out_file.write(content)
    return temp_file
