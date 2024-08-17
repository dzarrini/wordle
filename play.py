#!/usr/bin/python3

import sys
from wordle import best_word, answer_wordlist, guess

W_LENGTH = 5


# print(accept('RRYRY', 'speed', 'abide'))
# print(accept('YRYYR', 'speed', 'erase'))
# print(accept('GRGRR', 'speed', 'steal'))
# print(accept('RYGYR', 'speed', 'crepe'))

def pick_word(rst, available_words):
  for i in range(1, len(rst)):
    if rst[i-1][1] in available_words:
      return rst[i-1][1]
    if rst[i][0] != rst[i-1][0]:
      return rst[i-1][1]
  return rst[0][1]

def play():
  word = "salet"
  print(word)
  color = input("color: ")
  available_words = guess(color, word, answer_wordlist)
  print(available_words)
  if len(available_words) == 1:
    print(available_words[0])
    sys.exit(0)

  while True:
    words = best_word(available_words, 0)
    word = pick_word(words, available_words)
    print(word)
    color = input("color: ")
    available_words = guess(color, word, available_words)
    print(available_words)
    if len(available_words) == 1:
      print(available_words[0])
      sys.exit(0)

if __name__ == '__main__':
  # play()
  sys.exit(0)
