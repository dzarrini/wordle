#!/usr/bin/python3

from concurrent.futures import ProcessPoolExecutor, as_completed
from color import COLORS
import pickle

combined_wordlist = []
answer_wordlist = []

with open("words/combined_wordlist.txt", "r") as fi:
  for line in fi:
    combined_wordlist.append(line.rstrip())

with open("words/shuffled_real_wordles.txt", "r") as fi:
  for line in fi:
    answer_wordlist.append(line.rstrip())

def make_color(word, candidate):
  new_color = ''
  candidate = list(candidate)
  for i, (a,b) in enumerate(zip(word, candidate)):
    if a == b:
      new_color += 'G'
      candidate[i] = '*'
    elif a in candidate:
      new_color += 'Y'
      candidate[candidate.index(a)] = '*'
    else:
      new_color += 'R'
  return new_color

def make_color_word(word):
  rst = {}
  words_accepted_sz = 0
  for w in answer_wordlist:
    color = make_color(word, w)
    if color not in rst:
      rst[color] = set()
    rst[color].add(w)
  return rst

def build_word_color_map():
  rst = {}
  i = 1
  with ProcessPoolExecutor() as executor:
    futures = {executor.submit(
      make_color_word, word): word for word in combined_wordlist}
    for future in as_completed(futures):
      word = futures[future]
      try:
        result = future.result()
        print((i, word))
        i = i + 1
        rst[word] = result
      except Exception as exc:
        print(f"{word} generated an exception: {exc}")
  return rst

if __name__ == '__main__':
  rst = build_word_color_map()
  with open('word_color_bank.pkl', 'wb') as f:
    pickle.dump(rst, f)
