import uuid
import requests
import json
import re
import schedule
import time

url = "https://lb.dioco.io/base_items_itemsJsonExport_6"
url_anki_connect = 'http://localhost:8765'
deck = 'deck:Netflix'
model = 'LLNTemplate'

# extract data from languange reactor
def extract():
    try:
        print("Extract data from language reactor")
        # headers = {"Content-Type": "application/json; charset=utf-8"}

        # data = {
        #     "langCode_G": "en",
        #     "itemType": "WORD",
        #     "tags": [
        #         1
        #     ],
        #     "source": None,
        #     "loadMoreTimestamp": None,
        #     "loadMorePartNum": 1,
        #     "userEmail": "#",
        #     "diocoToken": "#"
        # }

        # reactor = requests.post(url, 
        #     json=data, 
        #     headers=headers,
        # ).json()

        # reactor_search = requests.get(reactor["data"]["file_path"]).json()
        reactor_search = requests.get("https://storage.googleapis.com/nlle-b0128.appspot.com/userExportCache/lln_json_items_2022-5-6_772588.json").json()    
        transform(reactor_search)

    except Exception as e:
        print(str(e))

def transform(reactor_search):
    try:
        print("start transform")
        words = []
        for data in reactor_search:
            temp = {}
            # transform and cleansing sentences
            word = data["word"]["text"]
            sentence = data["context"]["phrase"]["subtitles"]["1"]
            sentence = re.sub("\n", " ", sentence)
            sentence = re.sub("-", "", sentence)
            sentence = re.sub(r'\[[^()]*\]', "", sentence)
            sentence = re.sub(" +", " ", sentence)
            sentence = sentence.strip()
            sentence = sentence.capitalize()

            # sentence / subtitles 
            temp['sentence'] = sentence
            # word
            temp['word'] = word
            # mtranslations
            temp['translation'] = data["context"]["phrase"]["mTranslations"]["1"]
            # Video Title
            temp['video_title'] = data["context"]["phrase"]["reference"]["title"]
            # date created
            temp['date_created'] = data["timeModified_ms"]
            # video id
            temp['video_id'] = data["context"]["phrase"]["reference"]["movieId"]
            # source
            temp['source'] = data["context"]["phrase"]["reference"]["source"]
            # media
            temp['media'] = data["context"]["phrase"]["thumb_next"]["dataURL"]
            # tags
            # temp['tag'] = data["tags"]["0"]
            # audio
            temp['audio'] = data["audio"]["dataURL"]
            # translation
            temp['word_trans_arr'] = data["wordTranslationsArr"]
            
            words.append(temp.copy())
            
        load(words)
        print("end transform")

    except Exception as e:
        print(str(e))

def load(words):
    try:
        print("load data")
        matched = check_matched_word(words)

        print("stores data to anki")
        for word in words:
            for new in matched:
                if word["word"] == new:
                    # anki_store(word)
                    print(word["word"])
                    

    except Exception as e:
        print(str(e))

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
        r = requests.post('http://127.0.0.1:8765', json={
        "action": "addNote",
        "version": 6,
            "params": {
            "note": {
                "deckName": "Netflix",
                "modelName": model,
                "fields": {
                    "Item Key": str(uuid.uuid4()),
                    "Subtitle": word["sentence"],
                    "Video Title": word["video_title"],
                    "Lemma": word["word"],
                    "Source": word["source"],
                    "Audio Clip Media filename": ""
                },
                "options": {
                    "allowDuplicate": False
                },
                "tags": [
                    "TESTING"
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
    
def job():
    print("workers start")

    try:
        anki_conn()
        extract()
        print("successfully!")
    except Exception as e:
        print(str(e))

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)