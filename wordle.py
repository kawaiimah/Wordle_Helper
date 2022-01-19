# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 09:16:11 2022

Provides list of suggested words to try in Wordle
(https://www.powerlanguage.co.uk/wordle/)
based on frequency of letters appearing in the list
of potentially correct words based on the current
clues available (letters not in word, letters in
correct position, letters in wrong position)

"""

# read in word list
with open('word_list.txt') as f:
    words = set(f.read().split())

# filter for 5-letter words
words = [x for x in words if len(x)==5]

# update status of letters here
nope = '' # 'ae'
green = [] # [('p',1),('r',2),('o',3)]
yellow = [] # [('t',1),('r',2),('n',3),('i',4)]

# filter for words using only allowed letters
possible = []
for w in words:
    flag = True
    for c in w:
        if c in nope:
            flag = False
    if flag:
        possible.append(w)

# filter for words with correct letters in correct positions
possible1 = []
if green:
    for w in possible:
        flag = True
        for (c,p) in green:
            if c != w[p-1]:
                flag = False
        if flag:
            possible1.append(w)
else:
    possible1 = [w for w in possible]

# filter for words with correct letters in wrong positions
possible2 = []
if yellow:
    for w in possible1:
        flag = True
        for (c,p) in yellow:
            if c == w[p-1] or c not in w:
                flag = False
        if flag:
            possible2.append(w)
else:
    possible2 = [w for w in possible1]

# count occurrences of not-yet-tried letters
count = {}
temp = set([x[0] for x in yellow] + [x[0] for x in green])
for w in possible2:
    for c in w:
        if c not in temp:
            if c not in count:
                count[c] = 1
            else:
                count[c] += 1

# rank by frequency of not-yet-tried letters
rank = []
for w in possible2:
    score = 0
    for c in set(w):
        if c in count:
            score += count[c]
    rank.append((w,score))
ranksort = sorted(rank,key=lambda x:x[1],reverse=True)
cut = min(10,len(ranksort))
for r,s in ranksort[:cut]:
    print(f'{s}: {r}')

countsort = sorted([x for x in count.items()],key=lambda x:x[1],reverse=True)
cut = min(5,len(countsort))
print(countsort[:cut])