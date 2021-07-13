import json
import pandas as pd

with open('json_files/keychordmapping.json') as f:
    data = json.load(f)

def intersection(a, b):
    temp = set(b)
    c = [value for value in a if value in temp]
    return c

def ScoringModule(input_idx,input_name,chord_idx,chord_name,chord):
    score = 0
    idxMatch = intersection(input_idx,chord_idx)
    score += 10 * len(idxMatch)
    nameMatch = intersection(input_name,chord_name)
    score += 5 * len(nameMatch)
    if chord in ["I","II","III","IV","V","VI","VII"]:
        score +=1 
    if len(input_idx) != len(chord_idx):
        score -= 10
    return score

input_name = ["C","E","G"]
input_idx = [0,4,7]

chords = []
score = []
for entry in data:
    chords.append(entry["key"]+entry["chord"])
    score.append(ScoringModule(input_idx,input_name,entry["idx"],entry["naming"],entry["chord"]))
df = pd.DataFrame({"Chord":chords,"Score":score})
df = df.sort_values("Score",ascending=False)
print("The most likely chords are:")
print(df.head(10))





