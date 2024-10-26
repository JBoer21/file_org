from MNBclassifier import DocumentClassifier

def test_MNBclassifier_process():
    model = DocumentClassifier()
    names, contents, categories = model.process_folder('./testFall2024')

    print(model.predict("./testFall2024/TOC_hw3.pdf"))

test_MNBclassifier_process()