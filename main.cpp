#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <fstream>
#include <unordered_map>
#include <iomanip>
#include <thread>
#include <cmath>
#include <unistd.h>
#include <sys/wait.h>

using namespace std;

const int WORD_SIZE = 5;
const char* ANSWER_WORDLIST_PATH = "words/shuffled_real_wordles.txt";
const char* COMBINED_WORDLIST_PATH = "words/combined_wordlist.txt";
const hash<string> hasher;

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

std::unordered_map<std::string,std::unordered_map<std::string, string>> 
  build_color_map(
      const vector<string>& combined_wordlist, 
      const vector<string>& answer_wordlist) {
  std::unordered_map<std::string,std::unordered_map<std::string, string>> result;
  for(const auto& word: combined_wordlist) {
    for(const auto& candidate: answer_wordlist) {
      string color = make_color(word, candidate);
      result[word][candidate] = color;
    }
  }
  return result;
}

size_t get_hash(const vector<string>& words) {
  size_t hash = hasher(words[0]);
  for (size_t i = 1; i < words.size(); ++i) {
    hash ^= hasher(words[i]);
  }
  return hash;
}

double average_depth(
    const vector<string>& word_list,
    const vector<string>& combined_wordlist,
    const unordered_map<string, unordered_map<string,string>>& all_color_map,
    unordered_map<size_t, double>& memory_map) {
  double avg_depth_total = 1000;
  double avg_depth = 1000;
  double color_size;
  double depth;
  size_t hash;
  for (const auto& w : combined_wordlist) {
    std::unordered_map<std::string, vector<string>> color_map;
    for(const auto& candidate: word_list) {
      // string color = make_color(w, candidate);
      string color = all_color_map.at(w).at(candidate);
      color_map[color].push_back(candidate);
    }
    if (color_map.size() == 1) continue;
    if (color_map.size() == word_list.size()) {
      if (color_map.contains("GGGGG")) {
        return (1.0 + (word_list.size() - 1) * 2.0 ) / color_map.size();
      } else {
          return 2;
      }
    }
    color_size = color_map.size();
    depth = 0;
    for(const auto& [color, color_words] : color_map) {
      if (color == "GGGGG") {
        depth += 1;
      } else if (color_words.size() == 1) {
        depth += 2;
      } else if (color_words.size() == 2) {
        depth += 3;
      } else {
        hash = get_hash(color_words);
        if (auto search = memory_map.find(hash); search != memory_map.end()) {
          depth += (color_words.size() * search->second);
        } else {
          double d = average_depth(color_words, combined_wordlist, all_color_map, memory_map);
          memory_map[hash] = d;
          depth += (color_words.size() * d);
        }
      }
    }
    avg_depth = (depth / color_size);
    if ( avg_depth_total > avg_depth ) {
      avg_depth_total = avg_depth;
    }
  }
  return avg_depth_total;
}

double top_match(
    const vector<string>& first_depth,
    const vector<string>& word_list,
    const vector<string>& combined_wordlist,
    const unordered_map<string, unordered_map<string,string>>& all_color_map,
    unordered_map<size_t, double>& memory_map) {
  double avg_depth_total = 1000;
  double avg_depth = 1000;
  double color_size;
  double depth;
  size_t hash;
  for (const auto& w : first_depth) {
    std::unordered_map<std::string, vector<string>> color_map;
    for(const auto& candidate: word_list) {
      // string color = make_color(w, candidate);
      string color = all_color_map.at(w).at(candidate);
      color_map[color].push_back(candidate);
    }
    if (color_map.size() == 1) continue;
    if (color_map.size() == word_list.size()) {
      if (color_map.contains("GGGGG")) {
        return (1.0 + (word_list.size() - 1) * 2.0 ) / color_map.size();
      } else {
          return 2;
      }
    }
    color_size = color_map.size();
    cout << "Color Size: " << color_size << endl;
    depth = 0;
    for(const auto& [color, color_words] : color_map) {
      cout << "Started Color (" << color << "): " << color_words.size() << endl;
      if (color == "GGGGG") {
        depth += 1;
      } else if (color_words.size() == 1) {
        depth += 2;
      } else if (color_words.size() == 2) {
        depth += 3;
      } else {
        hash = get_hash(color_words);
        if (auto search = memory_map.find(hash); search != memory_map.end()) {
          depth += (color_words.size() * search->second);
        } else {
          double d = average_depth(color_words, combined_wordlist, all_color_map, memory_map);
          memory_map[hash] = d;
          depth += (color_words.size() * d);
        }
        // depth += color_words.size() + 1;
      }
      cout << "Finished Color (" << color << "): " << color_words.size() << ". ";
      cout << "Depth: " << depth << endl;
    }
    avg_depth = (depth / color_size);
    if ( avg_depth_total > avg_depth ) {
      avg_depth_total = avg_depth;
    }
  }
  return avg_depth_total;
}

vector<vector<string>> split_file(vector<string> words, int sz) {
  vector<vector<string>> results;
  vector<string> row;
  for(size_t i = 0; i < words.size(); ++i) {
    row.push_back(words[i]);
    if (i != 0 && i % sz == 0) {
      results.push_back(row);
      row.clear();
    }
  }
  results.push_back(row);
  return results;
}

int main() {
  auto answer_wordlist = read_words(ANSWER_WORDLIST_PATH);
  auto combined_wordlist = read_words(COMBINED_WORDLIST_PATH);
  auto color_map = build_color_map(combined_wordlist, answer_wordlist);
  unordered_map<size_t, double> memory_map;

  // auto results = split_file(combined_wordlist, 300);
  // pid_t* pids = new int[results.size()];
  // for (size_t i = 0; i < results.size(); ++i) {
  //   pids[i] = fork();
  //   if (pids[i] == 0) {
  //     top_match(answer_wordlist, combined_wordlist, results[i]);
  //     _exit(0);
  //   }
  // }

  // for (size_t i = 0; i < results.size(); ++i) {
  //   int status;
  //   pid_t pid = waitpid(pids[i], &status, 0);
  //   if (pid <= 0) {
  //     std::cerr << "Failed to wait for child " << i << std::endl;
  //   }
  // }

  cout << "Finished Building." << 10.982 << endl;
  cout << top_match({"salet"}, answer_wordlist, combined_wordlist, color_map, memory_map) << endl;
  cout << "Memory size: " << memory_map.size() << endl;
  // cout << make_color("speed", "abide") << endl;
  // cout << make_color("speed", "erase") << endl;
  // cout << make_color("speed", "steal") << endl;
  // cout << make_color("speed", "crepe") << endl;
  // auto world_color_map = build_word_color_map(combined_wordlist, answer_wordlist);
  // cout << setprecision (12) << average_matches(1,
  //     answer_wordlist, 
  //     answer_wordlist) << endl;
  // cout << setprecision (12) << average_matches(answer_wordlist, answer_wordlist) << endl;
  return 0;
}
