import os, sys

p = os.path.abspath("../modules")
sys.path.append(p)
from chordToNote import ChordToNote

# import numpy as np
import pandas as pd

major_keys = ["C", "G", "D", "A", "E", "B", "F", "Bb", "Eb", "Ab", "Db", "Gb"]
minor_keys = ["a", "e", "b", "f#", "c#", "g#", "d", "g", "c", "f", "bb", "eb"]

major_chords = [  # II, V, VII and DimVII seventh cancelled for now
    "I",
    "bII",
    "II",
    "III",
    "IV",
    "V",
    "bVI",
    "GerVI",
    "FreVI",
    "ItaVI",
    "VI",
    "VII",
]
minor_chords = [  # II V DimVII 7 cancel
    "I",
    "I+",
    "bII",
    "II",
    "III",
    "IV",
    "IV+",
    "V",
    "V+",
    "VI",
    "GerVI",
    "FreVI",
    "ItaVI",
    "VII",
    "DimVII",
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
