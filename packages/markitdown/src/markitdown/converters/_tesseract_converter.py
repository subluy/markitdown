"""Tesseract OCR converter for images to Markdown text extraction."""
from typing import BinaryIO, Any
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/bmp",
]

ACCEPTED_FILE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
]

# CJK Unicode ranges for post-processing (remove spaces between CJK chars)
_CJK_PATTERN = r"([一-鿿㐀-䶿豈-﫿　-〿＀-￯])[ ]+([一-鿿㐀-䶿豈-﫿　-〿＀-￯])"


class TesseractConverter(DocumentConverter):
    """Converts images to Markdown by extracting text with Tesseract OCR.

    Requires: pip install pytesseract Pillow
    Requires: Tesseract-OCR installed (https://github.com/UB-Mannheim/tesseract/wiki)
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        import os
        import re

        lang = kwargs.get("tesseract_lang", "eng+chi_sim")
        tesseract_cmd = kwargs.get("tesseract_cmd")
        tessdata_dir = kwargs.get("tesseract_tessdata_dir")

        try:
            from PIL import Image
            import pytesseract

            if tesseract_cmd:
                pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            if tessdata_dir:
                os.environ["TESSDATA_PREFIX"] = tessdata_dir

            image = Image.open(file_stream)
            text = pytesseract.image_to_string(
                image,
                lang=lang,
                config="--psm 6 -c preserve_interword_spaces=0",
            ).strip()

            # Remove single-character spaces between CJK characters
            # (a known Tesseract artifact for Chinese/Japanese/Korean)
            import re as _re
            for _ in range(5):
                new_text = _re.sub(_CJK_PATTERN, r"\1\2", text)
                if new_text == text:
                    break
                text = new_text

            return DocumentConverterResult(markdown=text)

        except ImportError:
            raise ImportError(
                "Tesseract OCR requires: pip install pytesseract Pillow\n"
                "Also install Tesseract-OCR: https://github.com/UB-Mannheim/tesseract/wiki"
            )
