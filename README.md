# Extractive Summarizer ,⌛ in progress

#### NLP-based extractive summarization using pretrained transformer models
> AI-powered extractive text summarization system

> using Sentence Transformers + MMR algorithm

<h1 id = 'requirements'>Requirements</h1>

- numpy
- scikit-learn
- sentence-transformers

# Create Virtual Enviroment
In first time of using, in project's folder open terminal:

```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

<a href = '#requirements'>requirements.txt </a>content

# How to use? 
1. Go to project file and open terminal(CMD)

2. Activate Virtual Enviroment in terminal.
```
.\venv\Scripts\activate
```

3. Determine the length of the summary in __main.py__ file Line 15.

``` python 
# change summary_size if you want
summary, idxs, scores = mmr_select(embs, sents, summary_size=3, lambda_param=0.7)
```
3. In terminal(CMD), run __grafical-UI.py__ (Make sure the Virtual Enviroment is activate):
```
python grafical-UI.py
```

4. Then enter your text and click summarize button.

5. You can watch the process in terminal(CMD) and summary text in GUI.