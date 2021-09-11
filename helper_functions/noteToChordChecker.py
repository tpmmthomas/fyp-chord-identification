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
    [["Ab", "C", "Eb", "Gb"], ""],
]

for tc in test_cases:
    keyinput = None if tc[1] == "" else tc[1]
    result = NoteToChord(tc[0], keyinput, 5)
    with open("../results/noteToChordResult.txt", "a") as f:
        f.write(
            f"For the notes {tc[0]}, with input key {str(keyinput)}, the results are:\n"
        )
        for i, ans in enumerate(result):
            f.write(
                f'{i}. {ans["Chord"]}, score: {ans["Score"]}, number of name match: {ans["name match"]}, number of pitch match: {ans["pitch match"]}, root present: {ans["root present"]}\n'
            )
        f.write("\n")

print("Done!")
