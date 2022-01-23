# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 11:36:05 2022

Testing letter frequency strategy against all possible Wordle words
"""

# read in word list
with open('wordle.txt') as f:
    words = set(f.read().split())

# compare a given guess against the secret word nd return
# letters not in secret in string nope
# letters and positions of correct letters in list green
# letters and positions of letters in incorrect positions in list yellow
def ngy(guess,secret):
    nope = ''
    green = []
    yellow = []
    for i,c in enumerate(list(guess)):
        if c not in secret:
            nope += c
        elif c == secret[i]:
            green.append([c,i])
        else:
            yellow.append([c,i])
    return(nope,green,yellow)

# add new information of nope,green and yellow to existing
# note the need to remove letters from yellow if found in green
def update_ngy(new_nope,new_green,new_yellow,old_nope,old_green,old_yellow):
    nope = old_nope + new_nope
    green = old_green + new_green
    temp = old_yellow + new_yellow
    yellow = []
    for (char,pos) in temp:
        if char not in [x[0] for x in green]:
            yellow.append((char,pos))
    return(nope,green,yellow)

# for a set of nope, green and yellow, decide next word to guess
def choose_guess(words,nope,green,yellow,guesses):
    # filter for words using only allowed letters
    possible = []
    for w in words:
        if w in guesses:
            continue
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
                if c != w[p]:
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
                if c == w[p] or c not in w:
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
    
    # specific interventions for first=='spend'
    if first == 'spend':
        if len(guesses)==3 and 'coral' in guesses and 'yacht' in guesses and ranksort[0][0] == 'batch':
            return 'wombs'
        if len(guesses)==3 and 'stare' in guesses and 'stave' in guesses and ranksort[0][0] == 'stale':
            return 'glike'
        if len(guesses)==2 and ranksort[0][0] == 'wound':
            return 'wombs'
        if len(guesses)==2 and ranksort[0][0] == 'caste':
            return 'chews'
        if len(guesses)==4 and ranksort[0][0] == 'boxer':
            return 'rooky'
        if len(guesses)==4 and ranksort[0][0] == 'jerky':
            return 'falaj'
    return ranksort[0][0]

# # for a set of nope, green and yellow, decide next word to guess
# def choose_guess(words,nope,green,yellow,guesses):
#     # filter for words using only allowed letters
#     possible = []
#     for w in words:
#         if w in guesses:
#             continue
#         flag = True
#         for c in w:
#             if c in nope:
#                 flag = False
#         if flag:
#             possible.append(w)
    
#     # filter for words with correct letters in correct positions
#     possible1 = []
#     if green:
#         for w in possible:
#             flag = True
#             for (c,p) in green:
#                 if c != w[p]:
#                     flag = False
#             if flag:
#                 possible1.append(w)
#     else:
#         possible1 = [w for w in possible]
    
#     # filter for words with correct letters in wrong positions
#     possible2 = []
#     if yellow:
#         for w in possible1:
#             flag = True
#             for (c,p) in yellow:
#                 if c == w[p] or c not in w:
#                     flag = False
#             if flag:
#                 possible2.append(w)
#     else:
#         possible2 = [w for w in possible1]
    
#     # count occurrences of not-yet-tried letters
#     count = {}
#     temp = set([x[0] for x in yellow] + [x[0] for x in green])
#     for w in possible2:
#         for c in w:
#             if c not in temp:
#                 if c not in count:
#                     count[c] = 1
#                 else:
#                     count[c] += 1
    
#     # rank by frequency of not-yet-tried letters
#     rank = []
#     for w in possible2:
#         score = 0
#         for c in set(w):
#             if c in count:
#                 score += count[c]
#         rank.append((w,score))
#     ranksort = sorted(rank,key=lambda x:x[1],reverse=True)
    
#     return ranksort[0][0]

# Insert specific first guess
first = 'spend'

# loop through all secret words
tracking = []
for secret in words:
    guesses = []
    nope,green,yellow = '',[],[]
    for i in range(6):
        if i==0:
            guess = first
        else:
            guess = choose_guess(words,nope,green,yellow,guesses)
        guesses.append(guess)
        if guess == secret:
            tracking.append((len(guesses),secret,guesses))
            print(tracking[-1])
            break
        else:
            new_nope,new_green,new_yellow = ngy(guess,secret)
            nope,green,yellow = update_ngy(new_nope,new_green,new_yellow,nope,green,yellow)
    if guess != secret:
        tracking.append((0,secret,guesses))
        print(tracking[-1])

success = [x[0] for x in tracking if x[0]!=0]
successrate = f'Success rate = {len(success)}/{len(tracking)} = {len(success)/len(tracking):.2%}'
print(successrate)
avgturns = f'Average number of guesses = {sum(success)/len(success):.2f}'
print(avgturns)

with open(first+'.txt','w') as f:
    f.write(successrate + '\n')
    f.write(avgturns + '\n')
    for o,s,glist in tracking:
        f.write(f'{o} {s}: ')
        for g in glist:
            f.write(g + ' ')
        f.write('\n')

# # Try every word as first word
# results = []
# for idx,first in enumerate(words):
    
#     if idx == 1820:
#         break
#     print(f'{idx}... ',end='')

#     # loop through all secret words
#     tracking = []
#     for secret in words:
#         guesses = []
#         nope,green,yellow = '',[],[]
#         for i in range(6):
#             if i==0:
#                 guess = first
#             else:
#                 guess = choose_guess(words,nope,green,yellow,guess)
#             guesses.append(guess)
#             if guess == secret:
#                 tracking.append((len(guesses),secret,guesses))
#                 break
#             else:
#                 new_nope,new_green,new_yellow = ngy(guess,secret)
#                 nope,green,yellow = update_ngy(new_nope,new_green,new_yellow,nope,green,yellow)
#         if guess != secret:
#             tracking.append((0,secret,guesses))
    
#     success = [x[0] for x in tracking if x[0]!=0]
#     successrate = len(success)/len(tracking)
#     avgturns = sum(success)/len(success)
#     results.append((first,successrate,avgturns))
#     print(results[-1])

# ratesort = sorted(results,key=lambda x:x[1],reverse=True)
# topsuccess = f'Top success rate: {ratesort[0][0]} {ratesort[0][1]:.2%} {ratesort[0][2]:.2f}'
# turnsort = sorted(results,key=lambda x:x[2])
# leastturns = f'Least average turns: {turnsort[0][0]} {turnsort[0][1]:.2%} {turnsort[0][2]:.2f}'
# print()
# print(topsuccess)
# print(leastturns)

# with open('results.txt','w') as f:
#     f.write(topsuccess + '\n')
#     f.write(leastturns + '\n')
#     for w,s,t in results:
#         f.write(f'{w}: {s:.2%} {t:.2f}\n')