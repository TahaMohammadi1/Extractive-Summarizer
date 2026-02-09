import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity  #similarity for two vector

SENT_PATH = "sentences.json"
EMB_PATH = "embedded.npy"

def load_data(sent_path=SENT_PATH, emb_path=EMB_PATH):
    with open(sent_path, "r", encoding="utf-8") as f:
        sents = json.load(f)
    embs = np.load(emb_path)
    return sents, embs

def compute_centroid(embs):
    # centroid = MEAN of vector's
    return np.mean(embs, axis=0, keepdims=True)

def mmr_select(embs, sents, summary_size=3, lambda_param=0.7):
    """
    return : 
    (summary_text, selected_indices, scores)
    """
    n = embs.shape[0]
    if summary_size >= n:
        #return all sentences
        return " ".join(sents), list(range(n)), [1.0]*n

    centroid = compute_centroid(embs)  # shape (1, D)
    sim_to_centroid = cosine_similarity(embs, centroid).reshape(-1)  # relevance

    selected_idx = []
    candidate_idx = list(range(n))
    # Precompute pairwise similarities between sentences for diversity calc
    pair_sim = cosine_similarity(embs, embs)  # n x n

    while len(selected_idx) < summary_size and candidate_idx:
        mmr_scores = []
        for i in candidate_idx:
            relevance = sim_to_centroid[i]
            if not selected_idx:
                diversity = 0.0
            else:
                # Max similarity of sentence i with other sentences
                diversity = max(pair_sim[i, j] for j in selected_idx)
            mmr_score = lambda_param * relevance - (1 - lambda_param) * diversity
            mmr_scores.append((mmr_score, i))
        # choose the best mmr
        mmr_scores.sort(reverse=True, key=lambda x: x[0])
        chosen = mmr_scores[0][1]
        selected_idx.append(chosen)
        candidate_idx.remove(chosen)

    # order of main text
    selected_idx_sorted = sorted(selected_idx)
    summary = " ".join([sents[i] for i in selected_idx_sorted])
    return summary, selected_idx_sorted, [float(sim_to_centroid[i]) for i in selected_idx_sorted]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=3, help="number of sentences in summary")
    parser.add_argument("--lambda_param", type=float, default=0.7, help="MMR lambda (0-1)")
    args = parser.parse_args()

    sents, embs = load_data()
    print(f"Loaded {len(sents)} sentences and embeddings shape {embs.shape}")
    summary, idxs, scores = mmr_select(embs, sents, summary_size=args.k, lambda_param=args.lambda_param)
    print("Selected sentence indices:", idxs)
    print("Relevance scores:", scores)
    print("\n=== SUMMARY ===\n")
    print(summary)
    # save
    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    print("\nSaved summary -> summary.txt")
