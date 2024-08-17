#!/usr/bin/python3

from concurrent.futures import ProcessPoolExecutor, as_completed
from color import COLORS

W_LENGTH = 5
FI = "combined_wordlist.txt"
combined_wordlist = []
answer_wordlist = []

with open("words/combined_wordlist.txt", "r") as fi:
  for line in fi:
    combined_wordlist.append(line.rstrip())

with open("words/shuffled_real_wordles.txt", "r") as fi:
  for line in fi:
    answer_wordlist.append(line.rstrip())

def accept(color, word, candidate):
  candidate = list(candidate)
  for i, (c, char) in enumerate(zip(color,word)):
    if c == "G":
      if char != candidate[i]:
        return False
      else:
        candidate[i] = "*"

  for i, (c, char) in enumerate(zip(color,word)):
    c = color[i]
    char = word[i]
    if c == "Y":
      if char not in candidate:
        return False
      else:
        candidate[candidate.index(char)] = "*"

  for i, (c, char) in enumerate(zip(color,word)):
    c = color[i]
    char = word[i]
    if c == "R":
      if char in candidate:
        return False
  return True

def guess(color, word, candidates):
  def accept_(candidate):
    return accept(color, word, candidate)
  return list(filter(accept_, candidates))


def num_matches(level, word, word_list):
  rst = 0
  total = len(word_list)
  print(total)
  words_accepted_sz = 0
  for color in COLORS:
    words_accepted = guess(color, word, word_list)
    words_accepted_sz = len(words_accepted)
    rst += ((words_accepted_sz / total) * (total - words_accepted_sz))
  return rst

def run(word):
  print(f'{word}: {num_matches(2,word, answer_wordlist)}')


def best_word(available_words, level):
  rst = []
  i = 1
  with ProcessPoolExecutor() as executor:
    futures = {executor.submit(
      num_matches, level, word, available_words): word for word in combined_wordlist}
    for future in as_completed(futures):
      word = futures[future]
      try:
        result = future.result()
        # print((i, result, word))
        i = i + 1
        rst.append((result, word))
      except Exception as exc:
        print(f"{word} generated an exception: {exc}")

  rst.sort(key=lambda tup: tup[0], reverse=True)
  return rst

if __name__ == '__main__':
  # print(best_word(answer_wordlist, 0)[0][1])
  run('roate')
