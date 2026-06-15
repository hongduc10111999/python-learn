import shutil

import pytesseract

_CANDIDATES = [
    "/opt/homebrew/bin/tesseract",
    "/usr/local/bin/tesseract",
    "/usr/bin/tesseract",
]


def configure_tesseract():
    found = shutil.which("tesseract")
    if found:
        pytesseract.pytesseract.tesseract_cmd = found
        return found
    for path in _CANDIDATES:
        if shutil.os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            return path
    return None


configure_tesseract()
