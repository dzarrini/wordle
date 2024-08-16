#!/usr/bin/python3

from concurrent.futures import ProcessPoolExecutor, as_completed

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

def num_matches(level, color, word, index, word_list, prob):
  total = len(word_list)

  if total == 0:
    return 0

  if index == W_LENGTH:
    # print(f'{word} {prob} ({color}): {word_list}')
    if level == 0:
      return 0
    max_score = 0
    for w in answer_wordlist:
      number = num_matches(level - 1,'', w, 0, word_list, 1)
      if number > max_score:
        max_score = number
    return prob * max_score

  wrd_green = []
  wrd_grey = []
  wrd_yellow = []

  char = word[index]
  for w in word_list:
    # This is green.
    if char == w[index]:
      wrd_green.append(w)
    elif char in w:
      wrd_yellow.append(w)
    elif char not in w:
      wrd_grey.append(w)

  def num_removed(c, list_of_interest):
    probability_picked = prob * len(list_of_interest) / total
    words_removed = total - len(list_of_interest)
    return (probability_picked * words_removed) + \
        num_matches(level, color + c, word, index + 1, list_of_interest, probability_picked)

  green_match = num_removed('G', wrd_green)
  grey_match = num_removed('R', wrd_grey)
  yellow_match = num_removed('Y', wrd_yellow)

  return green_match + grey_match + yellow_match

def run(word):
  print(f'{word}: {num_matches(2,"", word, 0, answer_wordlist, 1)}')

def best_word(available_words, level):
  rst = []
  i = 1
  with ProcessPoolExecutor() as executor:
    futures = {executor.submit(
      num_matches, level, "", word, 0, available_words, 1): word for word in combined_wordlist}
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
  print(best_word(answer_wordlist, 0)[0][1])
