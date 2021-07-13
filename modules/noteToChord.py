import json
import pandas as pd
import argparse

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

key_mapping={
    'C':0,
    'D':2,
    'E':4,
    'F':5,
    'G':7,
    'A':9,
    'B':11
}

#1 by 1 key to number
def key2num(key):  
  key=key.upper()
  num=key_mapping[key[0]]
  modifier=len(key)
  if modifier==1:
    return num
  elif key[1]=='#':
    return (num+(modifier-1))%12
  elif key[1]=='B':
    return (num-(modifier-1))%12
  elif key[1]=='X':
    return (num+(modifier-1)*2)%12

# key_list to number_list
def keys2num(keys):
  if keys[-1]=='-':
    return sorted([key2num(key) for key in keys[:-1]])
  else:
    return sorted([key2num(key) for key in keys])

def NoteToChord(input_name,numOut=10):
    chords = []
    score = []
    input_idx = keys2num(input_name)
    for entry in data:
        chords.append(entry["key"]+entry["chord"])
        score.append(ScoringModule(input_idx,input_name,entry["idx"],entry["naming"],entry["chord"]))
    df = pd.DataFrame({"Chord":chords,"Score":score})
    df = df.sort_values("Score",ascending=False)
    print("The most likely chords are:")
    print(df.head(numOut))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Output possible chords with given chord.")
    parser.add_argument("notes", nargs='+',help='The input keys (3 or 4 notes)')
    parser.add_argument("-o",'--numout',type=int,help='Number of output')
    parser.add_argument
    args = parser.parse_args()
    if args.numout is not None:
        NoteToChord(args.notes,args.numout)
    else:
        NoteToChord(args.notes)

