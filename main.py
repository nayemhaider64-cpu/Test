import argparse        æ
import mimetypes
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests
from tqdm import tqdm

DEFAULT_CHUNK_SIZE = 1024 * 10
USER_AGENT = "Mozilla/5.0 (compatible; PythonFileDownloader/1.0)"

def unique_path(file_path, overwrite=False):
    if overwrite or not file_path.exists():
        return file_path

    stem = file_path.stem
    suffix = file_path.suffix
    counter = 1

    while True:
        new_path = file_path.parent / f"{stem}({counter}){suffix}"

        if not new_path.exists():
            return new_path

        counter += 1


def content_disposition_filename(response):
    content_disposition = response.headers.get("Content-Disposition", "")

    match = re.search(r"filename\*=([^;]+)", content_disposition, flags=re.IGNORECASE)
    if match:
        value = match.group(1).strip().strip('"')
        if "''" in value:
            value = value.split("''", 1)[1]
        filename = unquote(value)
        if filename:
            return Path(filename).name

    match = re.search(r'filename="?([^";]+)"?', content_disposition, flags=re.IGNORECASE)
    if match:
        filename = Path(match.group(1)).name
        if filename:
            return filename

    return None


def file_name(response, url):
    filename = content_disposition_filename(response)
    if filename:
        return filename

    name = os.path.basename(urlparse(url).path)
    if name:
        return name

    content_type = response.headers.get("Content-Type", "").split(";")[0]
    suffix = mimetypes.guess_extension(content_type)
    if suffix:
        return f"download{suffix}"

    return "download"


def output_path_for(filename, output=None, overwrite=False):
    if output is None:
        file_path = Path.cwd() / filename
    else:
        output_path = Path(output)
        if output_path.exists() and output_path.is_dir():
            file_path = output_path / filename
        else:
            file_path = output_path

    file_path.parent.mkdir(parents=True, exist_ok=True)
    return unique_path(file_path, overwrite=overwrite)


def download_file(url, output=None, overwrite=False, chunk_size=DEFAULT_CHUNK_SIZE):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        filename = output_path_for(file_name(response, url), output, overwrite)
        total_size = int(response.headers.get("content-length", 0))

        with filename.open("wb") as file, tqdm(
            desc=filename.name,
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as progress:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
                    progress.update(len(chunk))

    return filename


def parse_args():
    parser = argparse.ArgumentParser(
        prog="download",
        description="Download any direct file URL with streaming and a progress bar.",
    )
    parser.add_argument("url", help="Direct URL of the file, image, video, or archive")
    parser.add_argument(
        "-o",
        "--output",
        help="Output filename or existing folder. Defaults to the current folder.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace the output file if it already exists.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help=f"Bytes read per streamed chunk. Default: {DEFAULT_CHUNK_SIZE}.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    download_file(
        args.url,
        output=args.output,
        overwrite=args.overwrite,
        chunk_size=args.chunk_size,
    )


if __name__ == "__main__":
    main()
