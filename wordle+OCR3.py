# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 09:16:11 2022

Provides list of suggested words to try in Wordle
(https://www.powerlanguage.co.uk/wordle/)
based on frequency of letters appearing in the list
of potentially correct words based on the current
clues available 

Includes use of OCR to auto-detect letters not in word, 
letters in correct position, letters in wrong position.
Optimised for Chrome browser 1920x1080 resolution

Further optimised to 100% success rate by setting first
guess to 'spend' with interventions to deal with a few
outlier cases
"""

import pyautogui
import pytesseract
import cv2
import numpy as np
import sys

# read in word list
with open('wordle.txt') as f:
    words = set(f.read().split())

# filter for 5-letter words
words = [x for x in words if len(x)==5]

# look for Wordle screen
print('\nRunning OCR...\n')
try:
    x, y = pyautogui.locateCenterOnScreen('wordle.png', confidence=0.8)
except:
    print('Wordle screen not found!')
    sys.exit()

# screengrab tile grid
x -= 207
y += 75
img_raw = pyautogui.screenshot(region=(x,y, 417, 505))

# convert to greyscale and invert to black and white
img_gray = cv2.cvtColor(np.array(img_raw), cv2.COLOR_RGB2GRAY)
(thresh, img) = cv2.threshold(img_gray, 250, 255, cv2.THRESH_BINARY)
img = np.invert(img)
# cv2.imwrite('img.png',img)

# crop to tiles
tile = []
for i in range(6):
    temp = []
    for j in range(5):
        temp.append(img[(i*83)+5:(i*80)+76,(j*83)+8:(j*80)+80].copy())
        # cv2.imwrite(f'tile{i}{j}.png',temp[-1])
    tile.append(temp)

# invoke tesseract for OCR
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
array = []
for i in range(6):
    temp = []
    for j in range(5):
        if np.sum(tile[i][j]) < 100_000:
            break
        try:
            char = pytesseract.image_to_string(tile[i][j], lang='eng', config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ')[:-2].upper()
            if char:
                temp.append(char[0])
            else:
                temp.append('I')
        except:
            temp.append('')
    if temp:
        array.append(temp)
    else:
        break

# get tile colors
color = []
guesses = []
for i,row in enumerate(array):
    guess = ''
    for j,char in enumerate(row):
        c = img_gray[(i*87)+5,(j*83)+8]
        if c < 133:
            cc = ('nope',j+1)
        elif c > 160:
            cc = ('yellow',j+1)
        else:
            cc = ('green',j+1)
        color.append((char,cc))
        guess += char
    guesses.append(guess)

color = sorted(color,key=lambda x:x[1][0])
print('Detected letters:')
for x in color:
    print(x)

# update status of letters
nope = ''
green = set([])
yellow = set([])
for char,(col,pos) in sorted(color,key=lambda x:x[1][0]):
    if col == 'nope':
        nope += char.lower()
    elif col == 'green':
        green.add((char.lower(),pos))
    else:
        ingreen = False
        for g in green:
            if char.lower() == g[0]:
                ingreen = True
        if not ingreen:
            yellow.add((char.lower(),pos))


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

suggest = ranksort[0][0]
# intervention to guess different letters for 2nd guess
if len(guesses) == 1:
    intervention = []
    for w in words:
        score = 0
        for c in set(w):
            if c in guess[0]:
                score -= 1000
            elif c in count:
                score += count[c]
        intervention.append((w,score))
    intervention = sorted(intervention,key=lambda x:x[1],reverse=True)
    suggest = intervention[0][0]

# intervention against testing one or two letters at a time
if len(guesses) in [3,4]:
    if len(green)+len(yellow) > 2 and len(ranksort) > 3:
        intervention = []
        for w in words:
            score = 0
            for c in set(w):
                if c in count:
                    score += count[c]
            intervention.append((w,score))
        intervention = sorted(intervention,key=lambda x:x[1],reverse=True)
        suggest = intervention[0][0]

print(f'\nSuggested guess: {suggest}')