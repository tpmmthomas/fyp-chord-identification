import os, sys

p = os.path.abspath("../modules")
sys.path.append(p)
from noteToChord import NoteToChord

# import numpy as np
import pandas as pd

test_cases = [
    [["C", "E", "G"], "CMajor"],
    [["Ab", "C", "Eb", "F#"], "CMajor"],
    [["C", "D", "G"], "CMajor"],
    [["Ab", "C", "Eb"], ""],
    [["C", "D", "E"], ""],
    [["A", "C", "E"], "Aminor"],
    [["A", "C", "E", "F", "G", "B"], "Aminor"],
    [["A", "C", "E", "F", "G", "B"], ""],
    [["Ab", "C", "Eb", "Gb", "G", "B"], ""],
]

major_chords = [
    "I",
    "bII",
    "II",
    "II7",
    "III",
    "IV",
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

pKey = []
pChord = []
pNote1 = []
pNote2 = []
pNote3 = []
pNote4 = []

for key in major_keys:
    key = key + "Major"
    for chord in major_chords:
        x = ChordToNote(key, chord)
        pKey.append(key)
        pChord.append(chord)
        pNote1.append(x[0])
        pNote2.append(x[1])
        pNote3.append(x[2])
        try:
            pNote4.append(x[3])
        except:
            pNote4.append("-")

for key in minor_keys:
    key = key + "Minor"
    for chord in minor_chords:
        x = ChordToNote(key, chord)
        pKey.append(key)
        pChord.append(chord)
        pNote1.append(x[0])
        pNote2.append(x[1])
        pNote3.append(x[2])
        try:
            pNote4.append(x[3])
        except:
            pNote4.append("-")

df = pd.DataFrame(
    {
        "Key": pKey,
        "Chord": pChord,
        "Note1": pNote1,
        "Note2": pNote2,
        "Note3": pNote3,
        "Note4": pNote4,
    }
)
df.to_csv("../results/chordToNoteResult.csv")
print("Done!")
