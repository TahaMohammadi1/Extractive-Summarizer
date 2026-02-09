import re

def clean_summary(text):
    # remove additional spaces 
    text = re.sub(r"\s+([,؛:؟!])", r"\1", text)
    # space after dot and symbols
    text = re.sub(r"([,؛:؟.!])([^\s])", r"\1 \2", text)
    # additional spaces
    text = re.sub(r"\s+", " ", text).strip()
    # Last dot .
    if len(text) > 0 and text[-1] not in ".؟!":
        text = text + "."
    return text