import os, sys

p = os.path.abspath("../modules")
sys.path.append(p)
from chordToNote import ChordToNote

# import numpy as np
import pandas as pd
import json

major_keys = ["C", "G", "D", "A", "E", "B", "F", "Bb", "Eb", "Ab", "Db", "Gb"]
minor_keys = ["a", "e", "b", "f#", "c#", "g#", "d", "g", "c", "f", "bb", "eb"]

major_chords = [
    "I",
    "I7",
    "bII",
    "II",
    "II7",
    "III",
    "III7",
    "IV",
    "IV7",
    "V",
    "V7",
    "bVI",
    "GerVI",
    "FreVI",
    "ItaVI",
    "VI",
    "VI7",
    "VII",
    "VII7",
    "DimVII7",
]
minor_chords = [
    "I",
    "I+",
    "bII",
    "II",
    "II7",
    "III",
    "IV",
    "IV+",
    "V",
    "V+",
    "V+7",
    "VI",
    "GerVI",
    "FreVI",
    "ItaVI",
    "VII",
    "DimVII",
    "DimVII7",
]


# json_list = []
# for key in major_keys:
#     key = key + "Major"
#     for chord in major_chords:
#         x,y = ChordToNote(key,chord)
#         json_list.append({"key":key,"chord":chord,"idx":x,"naming":y})

# for key in minor_keys:
#     key = key + "Minor"
#     for chord in minor_chords:
#         x,y = ChordToNote(key,chord)
#         json_list.append({"key":key,"chord":chord,"idx":x,"naming":y})

# with open('../modules/json_files/keychordmapping.json','w') as f:
#     json.dump(json_list,f)
json_list = {}
for key in major_keys:
    key = key + "Major"
    for chord in major_chords:
        x, y = ChordToNote(key, chord)
        json_list[key + chord] = {"idx": x, "naming": y, "chord": chord, "key": key}
for key in minor_keys:
    key = key + "Minor"
    for chord in minor_chords:
        x, y = ChordToNote(key, chord)
        json_list[key + chord] = {"idx": x, "naming": y, "chord": chord, "key": key}

with open("../modules/json_files/keychorddict.json", "w") as f:
    json.dump(json_list, f)

