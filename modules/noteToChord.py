import json
import pandas as pd
import argparse
import time

with open('json_files/keychordmapping.json') as f:
    data = json.load(f)

def intersection(a, b):
    temp = set(b)
    c = [value for value in a if value in temp]
    return c

def edit_distance(a,b):

    if len(a) > len(b):
        a = a[:-1]
    if len(b) > len(a):
        b = b[:-1]
    dist = 0
    for i,val in enumerate(a):
        dist += abs(val-b[i]) 
    ###Scoring function
    return 60//(dist+1)

def ScoringModule(input_idx,input_name,chord_idx,chord_name,chord):
    score = 0
    idxMatch = intersection(input_idx,chord_idx)
    score += 1000 * len(idxMatch)
    nameMatch = intersection(input_name,chord_name)
    score += 100 * len(nameMatch)
    score += edit_distance(input_idx,chord_idx)
    if chord in ["I"]:
        score +=4
    elif chord in ["IV","V"]:
        score += 3
    elif chord in ["II","VI"]:
        score += 2
    elif chord in ["III","VII"]:
        score += 1
    if len(input_idx) != len(chord_idx):
        score -= 100
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

# key_list to number_list
def keys2num(keys):
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
    if keys[-1]=='-':
        return [key2num(key) for key in keys[:-1]]
    else:
        return [key2num(key) for key in keys]

def NoteToChord(input_name,key=None,numOut=10):
    chords = []
    score = []
    input_idx = keys2num(input_name)
    for entry in data:
        if key is not None and entry["key"].upper() != key.upper():
            continue
        chords.append(entry["key"]+entry["chord"])
        score.append(ScoringModule(input_idx,input_name,entry["idx"],entry["naming"],entry["chord"]))
    df = pd.DataFrame({"Chord":chords,"Score":score})
    df = df.sort_values("Score",ascending=False)
    print("The most likely chords are:")
    print(df.head(numOut))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Output possible chords with given notes.")
    parser.add_argument("notes", nargs='+',help='The input keys (3 or 4 notes)')
    parser.add_argument("-o",'--numout',type=int,help='Number of output')
    parser.add_argument("-k","--key",help="The key (optional)")
    args = parser.parse_args()
    start = time.time()
    if args.numout is not None:
        NoteToChord(args.notes,args.key,args.numout)
    else:
        NoteToChord(args.notes,args.key)
    end = time.time()
    print("Time taken:",end-start)

