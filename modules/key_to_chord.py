import itertools

key_mapping={
    'C':0,
    'D':2,
    'E':4,
    'F':5,
    'G':7,
    'A':9,
    'B':11
}

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

# key_list to number_list
def keys2num(keys):
  if keys[-1]=='-':
    return sorted([key2num(key) for key in keys[:-1]])
  else:
    return sorted([key2num(key) for key in keys])


def keys2chords(keys,threshold=3):
  result=[]
  keys=keys2num(keys)
  keys=list(dict.fromkeys(keys)) #remove duplicates
  for i in range(threshold,5):
    for each in itertools.combinations(keys,i):
      result.extend(key_chord_name_mapping[str(each)])
  return result

#TEST
import time
answer=''
iterations=100000
start = time.time()
for i in range(iterations):
  answer=keys2chords(['C','E','G'],3)
end = time.time()
print((end - start)/iterations)

print(answer)