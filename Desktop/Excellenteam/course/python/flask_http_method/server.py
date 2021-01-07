from flask import Flask, Response, request
import json
import model 
# import requests

app = Flask(__name__)

@app.route('/sanity')
def sanity():
    return Response("Server up and running"), 200

@app.route('/words/<word_>')
def get_count_by_word(word_):
    res = {"count" : 0}
    if model.is_exist_word(word_):
        res["count"] = model.get_count_by_word(word_)

    return json.dumps(res), 200

def _insert_word(word):
    to_insert_word = ''.join(e for e in word if e.isalnum())
    model.insert_word(to_insert_word)
    text = "Added " + to_insert_word
    count = model.get_count_by_word(to_insert_word)
    return text, count

def _insert_sentence(sentence):
    numNewWords = 0
    numOldWords = 0
    for word in sentence.split(" "):
        word = word.lower()
        to_insert_word = ''.join(e for e in word if e.isalnum())
        if model.is_exist_word(to_insert_word):
            numOldWords += 1
        else:
            numNewWords += 1
        model.insert_word(to_insert_word)

    text = f"Added {numNewWords} words, {numOldWords} already existed"
    return text, -1

@app.route('/words', methods=["POST"])
def insert():
    text = ""
    counter = 0

    word = request.get_json().get("word")
    sentence = request.get_json().get("sentence")

    if word:
        word = word.lower()
        text, counter = _insert_word(word)
    if sentence:
        sentence = sentence.lower()
        text, counter = _insert_sentence(sentence)
    else:
        pass #rais exeption, len dic > 1

    res = {"text": text, "currentCount": counter}
    return json.dumps(res), 201

    
@app.route('/total')
def get_total_count():
    sum_ = model.get_total_counts()
    res = {"text": "Total count", "count": sum_}
    return json.dumps(res), 200

@app.route('/popular')
def get_popular():
    popular_word, count = model.get_popular_word()
    res = {"text": popular_word, "count": count }
    return json.dumps(res), 200

@app.route('/ranking')
def get_5_most_popular():
    most_populars = model.get_5_popular_words()
    lst_res = []
    for word, counter in most_populars:
        lst_res.append({word : counter})
    res = {"ranking": lst_res }
    return json.dumps(res), 200


@app.route('/words', methods=["PATCH"])
def update():
    req = request.get_json()
    to_updat = req["word"]
    new_word = req["updated"]
    if model.is_exist_word(to_updat):
        if not model.is_exist_word(new_word):
            model.update_word_key(to_updat, new_word)
            return json.dumps({"updated": new_word}), 200
        else:
            return json.dumps({"error": "The word is already exist"}), 500
    else:
        return json.dumps({"error": "The word is not found"}), 404



@app.route('/words', methods=["DELETE"])
def delete():
    word = request.get_json().get("word")
    if word:
        if model.is_exist_word(word):
            model.delete_word(word)
            return json.dumps({"deleted": word}), 200 #204
        else:
            return json.dumps({"error": "The word is not found"}), 404
    else:
        return json.dumps({"error": "Request's header not contain word key"}), 404


if __name__ == '__main__':
    app.run(port=1337)