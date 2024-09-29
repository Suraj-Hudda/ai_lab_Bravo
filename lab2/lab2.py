import numpy as np

def load_text(file_path):
    """Load text from a file."""
    with open(file_path, 'r') as file:
        return file.read()

def similarity_score(text1, text2):
    """Calculate the similarity score between two texts."""
    words1 = text1.split()
    words2 = text2.split()
    common_words = set(words1) & set(words2)
    return len(common_words) / (len(words1) + len(words2) - len(common_words))

def detect_plagiarism(doc_a, doc_b, threshold=0.3):
    """Detect plagiarism between two documents based on a similarity score."""
    score = similarity_score(doc_a, doc_b)
    return score > threshold, score

def main():
    """Main function to load documents and check for plagiarism."""
   
    doc_a = load_text('document_a.txt')
    doc_b = load_text('document_b.txt')
    doc_c = load_text('document_c.txt')

   
    result_ab, score_ab = detect_plagiarism(doc_a, doc_b)
    result_ac, score_ac = detect_plagiarism(doc_a, doc_c)

   
    print(f"Document A and Document B Plagiarized: {result_ab}, Similarity Score: {score_ab:.2f}")
    print(f"Document A and Document C Plagiarized: {result_ac}, Similarity Score: {score_ac:.2f}")

if __name__ == '__main__':
    main()
