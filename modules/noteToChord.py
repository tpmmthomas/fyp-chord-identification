import json
import pandas as pd
import argparse
import time
import itertools
import pickle

with open('json_files/keychorddict.json') as f:
    data = json.load(f)
with open('pickle_files/key_chord_name_mapping.pickle','rb') as f:
    key_chord_name_mapping = pickle.load(f)
for k in data:
  data[k]["key"]=(data[k]["key"].upper())

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
    if chord_idx[0] in input_idx:
        score += 500
    nameMatch = intersection(input_name,chord_name)
    score += 100 * len(nameMatch)
    if chord_name[0] in input_name:
        score += 50
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

def NoteToChord(keys_name,key=None,numOut=10,threshold=2):
    if numOut is None:
        numOut = 10
    if threshold is None:
        threshold = 2
    if key is not None:
        key=key.upper()
        
    keys_idx=keys2num(keys_name)
    sorted_keys = sorted(keys_idx)
    
    possible_chords=set()
    for i in range(threshold,5):
        for each in itertools.combinations(sorted_keys,i):
            possible_chords.update(key_chord_name_mapping[str(each)])
    chords = list(possible_chords)
    
    if chords == []:
        return None,None
    
    score = [-1 for temp in range(len(chords))]
    
    numOk = 0
    for idx in range(len(chords)):
        entry = data[chords[idx]]
        if key is None or entry["key"]==key:  ## make all key upper() after import**********
            score.append(ScoringModule(keys_idx,keys_name,entry["idx"],entry["naming"],entry["chord"]))
            numOk += 1

    score,chords=zip(*sorted(zip(score,chords),reverse=True)[:min(numOk,numOut)])
    return chords,score


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Output possible chords with given notes.")
    parser.add_argument("notes", nargs='+',help='The input keys (3 or 4 notes)')
    parser.add_argument("-o",'--numout',type=int,help='Number of output (optional)')
    parser.add_argument("-k","--key",help="The key (optional)")
    parser.add_argument("-t","--threshold",type=int,help='Least number of key matches (optional)')
    args = parser.parse_args()
    start = time.time()
    print(NoteToChord(args.notes,args.key,args.numout,args.threshold))
    end = time.time()
    print("Time taken:",end-start)

