import uuid
from regex import W
import requests
import json
import re
import schedule
import time
import mysql.connector

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
        #     "userEmail": "andy.natalino@gmail.com",
        #     "diocoToken": "GIZ0WjEIZTESi4BwgaCr6adukhX3MPj4n0Hiyu7kBSOHY3FvIot3eV8GxZmnemr06eUjlrhhExblc5LaZLOFiQ=="
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

            # sentence = re.sub(word, "<b>" + word + "</b>", sentence)

            print(sentence)

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
            temp['image'] = data["context"]["phrase"]["thumb_next"]["dataURL"]
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
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sentence_mining_db"
        )

        if db.is_connected():
            print("Success connected to database")
        
        print("load data")
        matched = check_matched_word(words)

        print("stores data to anki")
        for word in words:
            for new in matched:
                # print(word["image"])
                if word["word"] == new:

                    # check data database
                    cursor = db.cursor()
                    sql = """INSERT INTO words (item_key, subtitle, word, definition, trans, video_id, video_title, date_created, source, image, type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    values = [(
                        str(uuid.uuid4()), 
                        word["sentence"], 
                        word["word"], 
                        '-',
                        word["translation"], 
                        word["video_id"], 
                        word["video_title"], 
                        word["date_created"],
                        word["source"],
                        word["image"],
                        'api',
                    )]

                    # print(values)

                    for val in values:
                        cursor.execute(sql, val)
                        db.commit()
                
                    # print(word["word"])
                    # anki_store(word)
                    # print("***************************")
                    # print(word["word"])
                    # print("***************************")
                    

    except Exception as e:
        print("error", e)

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
    
def job():
    print("workers start")

try:
    anki_conn()
    extract()
    print("successfully!")
except Exception as e:
    print(str(e))

# schedule.every(1).minutes.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)