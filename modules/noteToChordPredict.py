from noteToChordWeighted import NoteToChord
import json

with open("../data/training_data.json", "r") as f:
    data = json.load(f)

for piece in list(data.keys()):
    chord_seq = data[piece]["chord_seq"]
    note_seq = data[piece]["note_seq"]
    print(chord_seq)
    print(note_seq)
    exit()
