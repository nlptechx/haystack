from pathlib import Path

from haystack.file_converter.pdf import PDFToTextConverter
from haystack.preprocessor.preprocessor import PreProcessor

TEXT = """
This is a sample sentence in paragraph_1. This is a sample sentence in paragraph_1. This is a sample sentence in 
paragraph_1. This is a sample sentence in paragraph_1. This is a sample sentence in paragraph_1.

This is a sample sentence in paragraph_2. This is a sample sentence in paragraph_2. This is a sample sentence in 
paragraph_2. This is a sample sentence in paragraph_2. This is a sample sentence in paragraph_2.

This is a sample sentence in paragraph_3. This is a sample sentence in paragraph_3. This is a sample sentence in 
paragraph_3. This is a sample sentence in paragraph_3. This is to trick the test with using an abbreviation like Dr. 
in the sentence. 
"""


def test_preprocess_sentence_split():
    document = {"text": TEXT}
    preprocessor = PreProcessor(split_length=1, split_stride=0, split_by="sentence")
    documents = preprocessor.process(document)
    assert len(documents) == 15

    preprocessor = PreProcessor(
        split_length=10, split_stride=0, split_by="sentence"
    )
    documents = preprocessor.process(document)
    assert len(documents) == 2


def test_preprocess_word_split():
    document = {"text": TEXT}
    preprocessor = PreProcessor(split_length=10, split_stride=0, split_by="word", split_respect_sentence_boundary=False)
    documents = preprocessor.process(document)
    assert len(documents) == 11

    preprocessor = PreProcessor(split_length=10, split_stride=0, split_by="word", split_respect_sentence_boundary=True)
    documents = preprocessor.process(document)
    for doc in documents:
        assert len(doc["text"].split(" ")) <= 10 or doc["text"].startswith("This is to trick")
    assert len(documents) == 15


def test_preprocess_passage_split():
    document = {"text": TEXT}
    preprocessor = PreProcessor(split_length=1, split_stride=0, split_by="passage", split_respect_sentence_boundary=False)
    documents = preprocessor.process(document)
    assert len(documents) == 3

    preprocessor = PreProcessor(split_length=2, split_stride=0, split_by="passage", split_respect_sentence_boundary=False)
    documents = preprocessor.process(document)
    assert len(documents) == 2


def test_clean_header_footer():
    converter = PDFToTextConverter()
    document = converter.convert(file_path=Path("samples/pdf/sample_pdf_2.pdf"))  # file contains header/footer

    preprocessor = PreProcessor(clean_header_footer=True, split_by=None)
    documents = preprocessor.process(document)

    assert len(documents) == 1

    assert "This is a header." not in documents[0]["text"]
    assert "footer" not in documents[0]["text"]
