from MNBclassifier import DocumentClassifier

def test_MNB_extract_file_data_docx():
    model = DocumentClassifier
    name, content = model.extract_data_from_file('./testing/test.docx')
    assert name == 'test'
    assert content == 'This is a test.'

def test_MNB_extract_file_data_pdf():
    model = DocumentClassifier
    name, content = model.extract_data_from_file('./testing/test.pdf')
    assert name == 'test'
    assert content == 'This is a test.'

def test_MNB_extract_file_data():
    test_MNB_extract_file_data_docx()
    test_MNB_extract_file_data_pdf()

test_MNB_extract_file_data()


