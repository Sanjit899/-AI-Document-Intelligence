import os
from pypdf import PdfReader

ALLOWED_EXTENSIONS = {"pdf"}


class PDFService:

    @staticmethod
    def allowed_file(filename: str) -> bool:
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def save_file(file, upload_folder: str) -> str:
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)
        return file_path

    @staticmethod
    def save_raw_file(contents: bytes, filename: str, upload_folder: str) -> str:
        os.makedirs(upload_folder, exist_ok=True)
        path = os.path.join(upload_folder, filename)

        with open(path, "wb") as f:
            f.write(contents)

        return path

    @staticmethod
    def extract_text(file_path: str) -> str:
        try:
            reader = PdfReader(file_path)
            text = ""

            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

            return PDFService.clean_text(text)

        except Exception as e:
            raise RuntimeError(f"Error reading PDF: {str(e)}")

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean weird characters and extra spaces
        """
        text = text.replace("\x00", " ")
        text = text.replace("\n\n", "\n")
        text = text.strip()
        return text
