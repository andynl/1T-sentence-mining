import uuid
import requests
import json

url_anki_connect = 'http://localhost:8765'
deck = 'deck:Netflix'
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

    return set(anki_data) ^ set(reactor_data)

def anki_conn():
    try:
        print("Connecting to AnkiConnect")
        res = requests.post(url_anki_connect, json={
            'action': 'findNotes',
            'version': 6,
            'params': {
                'query': deck,
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

def anki_store(word):
    try:
        r = requests.post(url_anki_connect, json={
        "action": "addNote",
        "version": 6,
            "params": {
            "note": {
                "deckName": "Netflix",
                "modelName": model,
                "fields": {
                    "Item Key": str(uuid.uuid4()),
                    "Subtitle": word["sentence"],
                    "Word": word["word"],
                    "Translation": word["translation"],
                    "Video ID": word["video_id"],
                    "Video Title": word["video_title"],
                    "Date Created": word["date_created"],
                    "Lemma": word["word"],
                    "Source": word["source"],
                    "Next Image Media Filename": "",
                    # "Audio Clip Media filename": ""
                },
                "options": {
                    "allowDuplicate": False
                },
                "tags": [
                    "green"
                ],
                "audio": {
                    "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
                    "filename": "yomichan_ねこ_猫.mp3",
                    "skipHash": "7e2c2f954ef6051373ba916f000168dc",
                    "fields": [
                        "Audio Clip Media filename"
                    ]
                }
            }
        }
        })

        print("New word: ", word["word"])
    except Exception as e:
        print(str(e))