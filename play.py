#!/usr/bin/python3

import sys
from wordle import best_word, answer_wordlist

W_LENGTH = 5

def accept(color, word, candidate, word_length=W_LENGTH):
  i = 0
  j = 0

  char_map = [-1] * 26
  for i in range(word_length):
    c = color[i]
    char = word[i]
    if c == "G":
      if char != candidate[i]:
        return False
      char_map[ord(char) - ord('a')] = i
    elif c == "Y":
      j = char_map[ord(char) - ord('a')] + 1
      y_match = False
      while j < W_LENGTH:
        if i == j or (j < word_length and color[j] == 'G'):
          j = j + 1
          continue
        if candidate[j] == char:
          y_match = True
          break
        j = j + 1
      if y_match is False:
        return False
      char_map[ord(char) - ord('a')] = j
    elif c == "R":
      j = char_map[ord(char) - ord('a')] + 1
      while j < word_length:
        if color[j] == 'G':
          j = j + 1
          continue
        if candidate[j] == char:
          return False
        j = j + 1
  return True

def guess(color, word, candidates):
  def accept_(candidate):
    return accept(color, word, candidate)
  return list(filter(accept_, candidates))

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
  play()
