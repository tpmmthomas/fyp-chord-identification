from noteToChordWeighted import NoteToChord
import json
import numpy as np

with open("../data/training_data2.json", "r") as f:
    data = json.load(f)

##PROVIDED KEY VERSION
total_accuracy = []
for piece in list(data.keys()):
    # print(piece)
    correct = 0
    total = 0
    chord_seq = data[piece]["chord_seq"]
    note_seq = data[piece]["note_seq"]
    print(chord_seq)
    print(note_seq)
    exit()
