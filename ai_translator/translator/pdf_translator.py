from typing import Optional
from translator.pdf_parser import PDFParser
from translator.writer import Writer
from translator.translation_chain import TranslationChain


class PDFTranslator:
    def __init__(self, model_name: str = "gpt-4o-mini", model_provider: str = "openai"):
        self.translation_chain = TranslationChain(
            model_name=model_name,
            model_provider=model_provider
        )
        self.pdf_parser = PDFParser()
        self.writer = Writer()

    def translate_pdf(self,
                      input_file: str,
                      output_file_format: str = 'markdown',
                      source_language: str = "English",
                      target_language: str = 'Chinese',
                      style: str = "standard",
                      pages: Optional[int] = None):

        self.book = self.pdf_parser.parse_pdf(input_file, pages)

        for page_idx, page in enumerate(self.book.pages):
            for content_idx, content in enumerate(page.contents):
                translation, status = self.translation_chain.run(
                    content,
                    source_language,
                    target_language,
                    style
                )
                self.book.pages[page_idx].contents[content_idx].set_translation(translation, status)

        return self.writer.save_translated_book(self.book, output_file_format)
