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

answer_wordlist_length = len(answer_wordlist)

word_color_map = None
with open("word_color_bank.pkl", "rb") as f:
  word_color_map = pickle.load(f)

def num_matches(word, color_map):
  rst = 0
  for available_words in color_map.values():
    n = len(available_words)
    rst += (n/answer_wordlist_length) * (answer_wordlist_length - n)
  return rst

def run(word):
  rst = num_matches(word, word_color_map[word])
  # print(f'{word}: {num_matches(word, word_color_map[word])}')
  return rst

def printer(results):
  for i in range(20):
    print(f'{results[i][1]}: {results[i][0]}')

def find_best_word():
  rst = []
  i = 1
  with ProcessPoolExecutor() as executor:
    futures = {executor.submit(
      run, word): word for word in combined_wordlist}
    for future in as_completed(futures):
      word = futures[future]
      try:
        result = future.result()
        print((i, word))
        i = i + 1
        rst.append((result, word))
      except Exception as exc:
        print(f"{word} generated an exception: {exc}")
  rst.sort(key=lambda tup: tup[0], reverse=True)
  printer(rst)
  return rst

if __name__ == '__main__':
  #   run('roate')
  find_best_word()
