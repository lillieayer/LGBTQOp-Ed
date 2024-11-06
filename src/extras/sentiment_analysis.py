from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from scipy.special import softmax
import csv
import urllib.request
import numpy as np
import urllib.request

def extract_sentiment():
    # Tasks:
    # most useful probs sentiment, emotion, offensive
    tasks = ['emoji', 'emotion', 'hate', 'irony', 'offensive', 'sentiment']
    task = 'sentiment'
    MODEL = f"cardiffnlp/twitter-roberta-base-{task}"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)

    # download label mapping
    labels=[]
    mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
    with urllib.request.urlopen(mapping_link) as f:
        html = f.read().decode('utf-8').split("\n")
        csvreader = csv.reader(html, delimiter='\t')
    labels = [row[1] for row in csvreader if len(row) > 1]

        # PT
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    #model.save_pretrained(MODEL)
    text = "I hate you"
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    print(f"output has dimens: ({scores.shape})")
    for i in range(scores.shape[0]):
        print(f"{labels[i]} --> {scores[i]}")

if __name__ == "__main__":

    extract_sentiment()
