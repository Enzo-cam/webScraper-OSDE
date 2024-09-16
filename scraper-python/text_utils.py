import unicodedata

class TextUtils:
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize Unicode text to ASCII."""
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

    @staticmethod
    def clean_text(text: str) -> str:
        """Remove extra whitespace and strip text."""
        return ' '.join(text.split()).strip()