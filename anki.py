import uuid
import requests
import json

url_anki_connect = 'http://localhost:8765'
deck = 'deck:English::Language Reactor'
model = 'LLNTemplate'

def check_matched_word(words):
    print("check matched word")
    anki_data = []
    anki = json.load(open("anki.json", "r"))
    for old in anki["result"]:
        anki_data.append(old["fields"]["Lemma"]["value"])

    reactor_data = []
    for new in words:
        reactor_data.append(new["word"])

    return set(reactor_data) & set(anki_data)

def anki_conn():
    try:
        print("Connecting to AnkiConnect")
        res = requests.post(url_anki_connect, json={
            'action': 'findNotes',
            'version': 6,
            'params': {
                'query': "deck:English",
            },
        }).json()

        if res.get('error', None):
            print('error:', res['error'])

        detail_res = requests.post(url_anki_connect, json={
            'action': 'notesInfo',
            'version': 6,
            'params': {
                'notes': res['result']
            },
        }).json()

        with open('anki.json', 'w') as fp:
            json.dump(detail_res, fp)

        print("Successfully stores anki data")
    except Exception as e:
        print(str(e))

def anki_store(word, item_key):
    try:
        filename = "{}.png".format(item_key)
        r = requests.post(url_anki_connect, json={
        "action": "addNote",
        "version": 6,
            "params": {
            "note": {
                "deckName": "English::Language Reactor",
                "modelName": model,
                "fields": {
                    "Word Definition": "-",
                    "Item Key": item_key,
                    "Subtitle": word["sentence"],
                    "Word": word["word"],
                    "Translation": word["translation"],
                    "Video ID": word["video_id"],
                    "Video Title": word["video_title"],
                    "Date Created": word["date_created"],
                    "Lemma": word["word"],
                    "Source": word["source"],
                    "Next Image Media Filename": filename,
                    # "Audio Clip Media filename": ""
                },
                "options": {
                    "allowDuplicate": False
                },
                "tags": [
                    "green"
                ],
            }
        }
        })
        print("New word: ", word["word"])
        print(r.json())
    except Exception as e:
        print(str(e))