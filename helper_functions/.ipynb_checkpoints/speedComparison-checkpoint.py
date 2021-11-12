import os,sys
p = os.path.abspath('../modules')
sys.path.append(p)
from noteToChord import NoteToChord
from noteToChordFast import NoteToChordFast
import time

start = time.time()
for i in range(1000):
    NoteToChord(['G','Bb','D','F'])
end = time.time()
print("Time taken (normal):", (end-start)/1000)

start = time.time()
for i in range(1000):
    NoteToChordFast(['G','Bb','D','F'])
end = time.time()
print("Time taken (fast):", (end-start)/1000)


'''
Test case 1: C E G
Time taken (normal): 0.00214697003364563
Time taken (fast): 0.0005820035934448242

Test Case 2: G Bb D F
Time taken (normal): 0.002198000431060791
Time taken (fast): 0.0005370192527770996
'''