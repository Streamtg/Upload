
import os
import time
import asyncio
from typing import Optional
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from config import Config

async def take_screen_shot(video_file : str, output_directory : str, ttl : float | int) -> Optional[str]:
    """
    Take Screenshot from Video.

    Source: https://stackoverflow.com/a/13891070/4723940

    :param video_file: Pass Video File Path.
    :param output_directory: Pass output folder path for screenshot. If folders not exists, this will create folders.
    :param ttl: Time!

    :return: This will return screenshot image path.
    """

    output_dir = f'{output_directory}/{time.time()}/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_filepath = output_dir + "thumbnail.jpeg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        output_filepath
    ]
    # width = "90"
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()

    # Petit ajout personnel
    if process.returncode != 0:
        # ffmpeg a échoué
        raise RuntimeError(f"FFmpeg error: {stderr.decode().strip()}")
    return output_filepath if os.path.lexists(output_filepath) else None

async def extract_duration(file_path : str) -> int :
    duration = 0
    parser = createParser(file_path)
    metadata = extractMetadata(parser)
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds
    parser.close()
    return duration