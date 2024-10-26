from MNBclassifier import DocumentClassifier

def test_MNBclassifier_process():
    model = DocumentClassifier()
    names, contents, categories = model.process_folder('./testFall2024')

test_MNBclassifier_process()