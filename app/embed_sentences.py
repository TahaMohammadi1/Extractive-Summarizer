import sys
import re
from sentence_transformers import SentenceTransformer
import json
import numpy as np

def sentences_split(text):
    # split with symbol's
    sentences = re.split(r'(?<=[.!؟])\s+', text)
    # remove empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def embed_and_save(input_path):
    output_sentences_path = "sentences.json"
    output_embeded_path = "embeded.npy"

    # read text
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # split senteneces 
    sentences = sentences_split(text) 
    print(f"Found {len(sentences)} sentences.")

    # load sentence transformers model
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
    embeddings = model.encode(sentences, show_progress_bar=True) 

    # save splited sentences
    with open(output_sentences_path, "w", encoding="utf-8") as f:
        json.dump(sentences, f, ensure_ascii=False, indent=2)

    # save embeddings
    np.save(output_embeded_path, embeddings)

    print(f"detected sentences saved in {output_sentences_path} file.")
    print(f"embeddings saved in {output_embeded_path} file")
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception ("not enough arguman's")
    
    input_path = sys.argv[1]
    embed_and_save(input_path)
