#!/usr/bin/python3

W_LENGTH = 5
# FI = "wordlist.txt"
FI = "combined_wordlist.txt"
word_list = []
answers = []


for line in open(FI, "r"):
  word_list.append(line.rstrip())

for line in open("shuffled_real_wordles.txt", "r"):
  answers.append(line.rstrip())

def num_matches(word, index, word_list, prob):
  total = len(word_list)

  if index == W_LENGTH:
    return 0

  if total == 0:
    return 0

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

  def num_removed(color, list_of_interest):
    probability_picked = prob * len(list_of_interest) / total
    words_removed = total - len(list_of_interest)
    return (probability_picked * words_removed) + num_matches(word, index + 1, list_of_interest, probability_picked)

  green_match = num_removed("green", wrd_green)
  grey_match = num_removed("yellow", wrd_grey)
  yellow_match = num_removed("grey", wrd_yellow)

  return green_match + grey_match + yellow_match

def run(word):
  print(f'{word}: {num_matches(word, 0, word_list)}')

def best_word(available_words):
  max_score = 0
  best_word = None
  rst = []
  for word in word_list:
    number = num_matches(word, 0, available_words, 1)
    rst.append((number, word))
    if number > max_score:
      max_score = number
      best_word = word

  rst.sort(key=lambda tup: tup[0], reverse=True)
  # for i in range(min(16,len(rst))):
  #   print(f'{i+1}.{rst[i][1]}: ({len(available_words) - rst[i][0]})')
  return best_word


def guess(color, word, all_words):
  old_words = all_words
  new_words = []
  for i in range(W_LENGTH):
    c = color[i]
    if c == "G":
      for w in old_words:
        if w[i] == word[i]:
          new_words.append(w)
    elif c == "R":
      for w in old_words:
        if word[i] not in w[i:]:
          new_words.append(w)
    elif c == "Y":
      for w in old_words:
        if w[i] != word[i] and word[i] in w:
          new_words.append(w)
    if len(new_words) == 0:
      return old_words
    old_words = new_words
    new_words = []
  return old_words


def play():
  WORD = "roate"
  print(WORD)
  color = input("color: ")
  all_words = guess(color, WORD, answers)
  if len(all_words) == 1:
    print(all_words[0])
    exit(0)

  while True:
    word = best_word(all_words)
    color = input("color: ")
    all_words = guess(color, word, all_words)
    print(all_words)
    if len(all_words) == 1:
      print(all_words[0])
      exit(0)

# print(best_word(answers))
print(best_word(word_list))
# play()
