from collections import Counter

wordCounter = {"word_name": 2}

def is_exist_word(word):
    if wordCounter.get(word):
        return True
    return False

def get_count_by_word(word):
    return wordCounter.get(word)

def get_total_counts():
    sum_ = 0
    for cnt in wordCounter.values():
        sum_ += cnt
    return sum_

def get_popular_word():
    max_ = 0
    word = ""
    for key, val in wordCounter.items():
        if val > max_:
            word = key
            max_ = val
    return word, max_

def get_5_popular_words():
    return Counter(wordCounter).most_common(5)

def insert_word(word):
    if wordCounter.get(word):
        wordCounter[word] += 1
    else:
        wordCounter[word] = 1

def delete_word(word):
    del wordCounter[word]

def update_word_key(word, new_word):
    cnt = wordCounter[word]
    del wordCounter[word]
    wordCounter[new_word] = cnt
