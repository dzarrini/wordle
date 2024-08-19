#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <fstream>
#include <unordered_map>
#include <iomanip>
#include <thread>
#include <cmath>

using namespace std;

const int WORD_SIZE = 5;
const char* ANSWER_WORDLIST_PATH = "words/shuffled_real_wordles.txt";
const char* COMBINED_WORDLIST_PATH = "words/combined_wordlist.txt";

vector<string> read_words(const char* file_path) {
  ifstream fi (file_path, ifstream::in);
  string line;
  vector<string> words;
  if (!fi.is_open()) {
    cerr << "failed to open file:" << file_path << endl;
    return words;
  }
  while(getline(fi,line)) {
    words.push_back(line);
  }
  fi.close();
  return words;
}

std::string make_color(const string& word, string candidate) {
  string color(' ',WORD_SIZE);
  int j;
  bool found;
  for (int i = 0; i < WORD_SIZE; ++i) {
    if (word[i] == candidate[i]) {
      color[i] = 'G';
    } else {
      found = false;
      for(j = 0; j < WORD_SIZE; ++j) {
        if (i == j) {
          continue;
        }
        if (word[i] == candidate[j]) {
          found = true;
          color[i] = 'Y';
          candidate[j] = '*';
        }
      }
      if (found == false) {
        color[i] = 'R';
      }
    }
  }
  return color;
}

std::unordered_map<std::string,std::unordered_map<std::string, vector<string>>> 
  build_word_color_map(
      const vector<string>& combined_wordlist, 
      const vector<string>& answer_wordlist) {
  std::unordered_map<std::string,std::unordered_map<std::string, vector<string>>> result;
  for(const auto& word: combined_wordlist) {
    for(const auto& candidate: answer_wordlist) {
      string color = make_color(word, candidate);
      result[word][color].push_back(candidate);
    }
  }
  return result;
}

double average_matches(
    const vector<string>& word_list,
    const string& word) {
  if (word_list.empty()) {
    return 0;
  }
  if (word_list.size() == 1) {
    return 1;
  }
  if (word_list.size() == 2) {
    return 1;
  }
  double sz = word_list.size();
  std::unordered_map<std::string, vector<string>> color_map;
  for(const auto& candidate: word_list) {
    string color = make_color(word, candidate);
    color_map[color].push_back(candidate);
  }
  if (color_map.size() == sz) {
    return 0;
  }
  double result = 0;
  double words_sz = 0;
  for(const auto& [color, words] : color_map) {
    if (words.empty()) {
      continue;
    }
    words_sz = words.size();
    result += (words_sz / sz) * ( words_sz);
  }
  return result;
}

double average_matches(
    int level,
    const vector<string>& word_list,
    const vector<string>& combined_wordlist) {
  if (word_list.empty()) {
    return 0;
  }
  if (word_list.size() == 1) {
    return 1;
  }
  if (word_list.size() == 2) {
    return 1;
  }
  double sz = word_list.size();
  string best_word;
  double best_rst = 20000;
  for (const auto& w : combined_wordlist) {
    std::unordered_map<std::string, vector<string>> color_map;
    for(const auto& candidate: word_list) {
      string color = make_color(w, candidate);
      color_map[color].push_back(candidate);
    }
    if (color_map.size() == sz) {
      return 0;
    }
    double result = 0;
    double words_sz = 0;
    for(const auto& [color, words] : color_map) {
      if (words.empty()) {
        continue;
      }

      // cout << color << ", " << words.size() << endl;
      words_sz = words.size();
      if (level == 0) {
        result += (words_sz / sz) * ( words_sz );
      } else {
        result += (words_sz / sz) * ( average_matches(
              level - 1,
              words,
              combined_wordlist));
      }
    }
    if (level == 1) {
      cout << setprecision (10) << result << ": " << w << endl;
    }
    if (result < best_rst) {
      best_rst = result;
      best_word = w;
    }
    if (abs(1 - best_rst) < 0.00001) {
      return 1;
    }
  }
  return best_rst;
}

int main() {
  auto answer_wordlist = read_words(ANSWER_WORDLIST_PATH);
  auto combined_wordlist = read_words(COMBINED_WORDLIST_PATH);

  // cout << make_color("speed", "abide") << endl;
  // cout << make_color("speed", "erase") << endl;
  // cout << make_color("speed", "steal") << endl;
  // cout << make_color("speed", "crepe") << endl;
  // auto world_color_map = build_word_color_map(combined_wordlist, answer_wordlist);
  // cout << setprecision (12) << average_matches(1,
  //     answer_wordlist, 
  //     answer_wordlist) << endl;
  cout << setprecision (12) << average_matches(1,
      answer_wordlist, 
      combined_wordlist) << endl;
  // cout << setprecision (12) << average_matches(answer_wordlist, answer_wordlist) << endl;
  cout << setprecision (12) << average_matches(answer_wordlist, "raise") << endl;
  return 0;
}
