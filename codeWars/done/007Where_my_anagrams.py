# https://www.codewars.com/kata/523a86aa4230ebb5420001e1/train/python
"""
What is an anagram? Well, two words are anagrams of each other if they both contain the same letters. For example:
'abba' & 'baab' == true
'abba' & 'bbaa' == true
'abba' & 'abbba' == false
'abba' & 'abca' == false
Write a function that will find all the anagrams of a word from a list. You will be given two inputs a word and an array
with words. You should return an array of all the anagrams or an empty array if there are none. For example:
anagrams('abba', ['aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada']) => ['aabb', 'bbaa']
anagrams('racer', ['crazer', 'carer', 'racar', 'caers', 'racer']) => ['carer', 'racer']
anagrams('laser', ['lazing', 'lazy',  'lacer']) => []
"""


# test.assert_equals(anagrams('abba', ['aabb', 'abcd', 'bbaa', 'dada']), ['aabb', 'bbaa'])

def anagrams1(word, words):
  return [w for w in words if sorted([c for c in word]) == sorted([c for c in w])]


def anagrams2(word, words):
  return [w for w in words if sorted(word) == sorted(w)]
  
  
def anagrams3(word,words):
  a = []
  s_word = sorted(set(word))
  a.append([w for w in words if s_word == sorted(set(w))])
  return a

def anagrams4(word,words):
  return [w for w in words if sorted(set(word)) == sorted(set(w))]


 
def ana1(w1,w1l,w2,w2l,w3,w3l):
  tbl = []

  tbl.append(anagrams1(w1,w1l))

  tbl.append(anagrams1(w2,w2l))

  tbl.append(anagrams1(w3,w3l))
  
  print(tbl)


def ana2(w1,w1l,w2,w2l,w3,w3l):
  tbl = []

  tbl.append(anagrams2(w1,w1l))

  tbl.append(anagrams2(w2,w2l))

  tbl.append(anagrams2(w3,w3l))
  
  print(tbl)


def ana3(w1,w1l,w2,w2l,w3,w3l):
  tbl = []

  tbl.append(anagrams3(w1,w1l))

  tbl.append(anagrams3(w2,w2l))

  tbl.append(anagrams3(w3,w3l))
  
  print(tbl)


def ana4(w1,w1l,w2,w2l,w3,w3l):
  tbl = []

  tbl.append(anagrams4(w1,w1l))

  tbl.append(anagrams4(w2,w2l))

  tbl.append(anagrams4(w3,w3l))
  
  print(tbl)

w1 = 'abba'
w1l = ['aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada','aabb', 'abcd', 'bbaa', 'dada']
w2 = 'racer'
w2l = ['crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar', 'crazer', 'carer', 'racar']
w3 = 'laser'
w3l = ['lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing', 'lazy', 'lacer', 'lazing', 'lazy', 'lazing']

print('====== anagram 1 ======')
ana1(w1,w1l,w2,w2l,w3,w3l)
print('====== anagram 2 ======')
ana2(w1,w1l,w2,w2l,w3,w3l)
print('====== anagram 3 ======')
ana3(w1,w1l,w2,w2l,w3,w3l)
print('====== anagram 4 ======')
ana4(w1,w1l,w2,w2l,w3,w3l)

