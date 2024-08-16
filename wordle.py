#!/usr/bin/python3

W_LENGTH = 5
# FI = "wordlist.txt"
FI = "combined_wordlist.txt"
word_list = []
answers = []

from concurrent.futures import ProcessPoolExecutor, as_completed

for line in open(FI, "r"):
  word_list.append(line.rstrip())

for line in open("shuffled_real_wordles.txt", "r"):
  answers.append(line.rstrip())

def num_matches(level, color, word, index, word_list, prob):
  total = len(word_list)

  if total == 0:
    return 0

  if index == W_LENGTH:
    # print(f'{word} {prob} ({color}): {word_list}')
    if level == 0:
      return 0
    max_score = 0
    for w in answers:
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
    return (probability_picked * words_removed) + num_matches(level, color + c, word, index + 1, list_of_interest, probability_picked)

  green_match = num_removed('G', wrd_green)
  grey_match = num_removed('R', wrd_grey)
  yellow_match = num_removed('Y', wrd_yellow)

  return green_match + grey_match + yellow_match

def run(word):
  print(f'{word}: {num_matches(1,"", word, 0, answers, 1)}')

# run('roate')

def best_word(available_words, level):
  max_score = 0
  best_word = None
  rst = []
  i = 1
  with ProcessPoolExecutor() as executor:
    futures = {executor.submit(num_matches, level, "", word, 0, available_words, 1): word for word in word_list}
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
  for i in range(min(20, len(rst))):
    print(f'{i+1}.{rst[i][1]}: ({len(available_words) - rst[i][0]})')
  return rst[0][1]

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
      if y_match == False:
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

def play():
  WORD = "salet"
  print(WORD)
  color = input("color: ")
  all_words = guess(color, WORD, answers)
  print(all_words)
  if len(all_words) == 1:
    print(all_words[0])
    exit(0)

  while True:
    word = best_word(all_words, 1)
    # print(word)
    color = input("color: ")
    all_words = guess(color, word, all_words)
    print(all_words)
    if len(all_words) == 1:
      print(all_words[0])
      exit(0)

# print(best_word(answers, 1))
# print(best_word(word_list))
play()
