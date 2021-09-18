import pandas as pd
import numpy as np
import itertools
import pickle

key_mapping = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

# 1 by 1 key to number
def key2num(key):
    key = key.upper()
    num = key_mapping[key[0]]
    modifier = len(key)
    if modifier == 1:
        return num
    elif key[1] == "#":
        return (num + (modifier - 1)) % 12
    elif key[1] == "B":
        return (num - (modifier - 1)) % 12
    elif key[1] == "X":
        return (num + (modifier - 1) * 2) % 12


def keys2num(keys):
    if keys[-1] == "-":
        return sorted([key2num(key) for key in keys[:-1]])
    else:
        return sorted([key2num(key) for key in keys])


df = pd.read_csv("../results/chordToNoteResult.csv")
df_copy = df.copy()
df_copy = df_copy.drop(["Unnamed: 0", "Key", "Chord"], axis=1)

# array: store every chord's key in the same order wrt the csv file
known_key = list(df_copy.to_numpy())
for idx in range(len(known_key)):
    known_key[idx] = sorted(keys2num(known_key[idx]))

# Return whether given arr is a subset of a array in list_arrays
def subset_in_list(arr, list_arrays):
    for array in list_arrays:
        for each in arr:
            if not (each in array):
                break
        else:
            return True
    return False


# all combinations of 4 key notes
combination = np.array(
    list(
        itertools.chain.from_iterable(
            itertools.combinations(np.arange(12), n) for n in range(5)
        )
    )
)


# array: possible chord_idx in the same order wrt combination
key_chord_idx = []
for combo in combination:
    chord = []
    for chord_idx in range(len(known_key)):
        for note in combo:
            if not (note in known_key[chord_idx]):
                break
        else:
            chord.append(chord_idx)
    key_chord_idx.append(chord)

# key --> chord_idx mapping :
key_chord_mapping = {}
for idx in range(len(combination)):
    key_chord_mapping[str(combination[idx])] = key_chord_idx[idx]

# key --> chord_name mapping :
key_chord_name_mapping = {}
for key in key_chord_mapping:
    key_chord_name_mapping[key] = [
        "".join(df.loc[idx, ["Key", "Chord"]].tolist())
        for idx in key_chord_mapping[key]
    ]


with open("../modules/pickle_files/key_chord_mapping.pickle", "wb") as handle:
    pickle.dump(key_chord_mapping, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open("../modules/pickle_files/key_chord_name_mapping.pickle", "wb") as handle:
    pickle.dump(key_chord_name_mapping, handle, protocol=pickle.HIGHEST_PROTOCOL)
