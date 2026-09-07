import io
import os

from gtts import gTTS
from pypdf import PdfReader

SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "pt": "Portuguese",
}


def read_file(filename):
    extension = os.path.splitext(filename)[1].lower()

    if extension == ".txt":
        with open(filename, "r", encoding="utf-8-sig") as file:
            return file.read().strip()

    if extension == ".pdf":
        reader = PdfReader(filename)

        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        ).strip()

    raise ValueError(
        "Only .txt and .pdf files are supported."
    )


def split_text(text, limit=4000):
    chunks = []

    while text:
        if len(text) <= limit:
            chunks.append(text)
            break

        position = text.rfind(" ", 0, limit)

        if position == -1:
            position = limit

        chunks.append(text[:position])
        text = text[position:].lstrip()

    return chunks


def convert_file(input_file, language="en"):
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported language. Choose from: {list(SUPPORTED_LANGUAGES.keys())}"
        )

    if not os.path.isfile(input_file):
        raise FileNotFoundError(
            f"File not found: {input_file}"
        )

    output_file = (
        os.path.splitext(input_file)[0] + ".mp3"
    )

    text = read_file(input_file)

    if not text:
        raise ValueError("No text found in the file.")

    chunks = split_text(text)

    with open(output_file, "wb") as output:
        for chunk in chunks:
            audio = io.BytesIO()

            gTTS(
                text=chunk,
                lang=language,
                slow=False,
            ).write_to_fp(audio)

            audio.seek(0)
            output.write(audio.read())

    return output_file
