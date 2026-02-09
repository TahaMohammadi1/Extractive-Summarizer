import sys
from summarizer import mmr_select, load_data
from postprocess import clean_summary

def main():

    #Load sentences & embeddings 
    try:
        sents, embs = load_data()
    except FileNotFoundError:
        print("Error: sentences.json or embedded.npy not found.")
        sys.exit(1)

    # Choose important sentences with MMR
    summary, idxs, scores = mmr_select(embs, sents, summary_size=3, lambda_param=0.7)

    # Post-process
    summary_clean = clean_summary(summary)

    # Output on terminal
    print("\n=== SUMMARY ===\n")
    print(summary_clean)
    print("\nSelected sentence indices:", idxs)
    print("Relevance scores:", scores)

    # save summary
    with open("app/summary.txt", "w", encoding="utf-8") as f:
        f.write(summary_clean)
    print("\nSaved summary -> app/summary.txt")

if __name__ == "__main__":
    main()
