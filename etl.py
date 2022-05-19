import requests
import re
import schedule
import time

from database import connection, get_word, store_word
from anki import check_matched_word, anki_conn,anki_store

url = "https://lb.dioco.io/base_items_itemsJsonExport_6"

# extract data from languange reactor
def extract():
    try:
        print("Extract data from language reactor")
        headers = {"Content-Type": "application/json; charset=utf-8"}

        data = {
            "langCode_G": "en",
            "itemType": "WORD",
            "tags": [
                1
            ],
            "source": None,
            "loadMoreTimestamp": None,
            "loadMorePartNum": 1,
            "userEmail": "andy.natalino@gmail.com",
            "diocoToken": "GIZ0WjEIZTESi4BwgaCr6adukhX3MPj4n0Hiyu7kBSOHY3FvIot3eV8GxZmnemr06eUjlrhhExblc5LaZLOFiQ=="
        }

        # reactor = requests.post(url, 
        #     json=data, 
        #     headers=headers,
        # ).json()

        # reactor_search = requests.get(reactor["data"]["file_path"]).json()
        reactor_search = requests.get("https://storage.googleapis.com/nlle-b0128.appspot.com/userExportCache/lln_json_items_2022-5-6_772588.json").json()    
        transform(reactor_search)

    except Exception as e:
        print('ERROR Extract', str(e))

def transform(reactor_search):
    try:
        print("start transform")
        words = []
        for data in reactor_search:
            temp = {}
            word = data["word"]["text"]
            sentence = data["context"]["phrase"]["subtitles"]["1"]
            sentence = re.sub("\n", " ", sentence)
            sentence = re.sub("-", "", sentence)
            sentence = re.sub(r'\[[^()]*\]', "", sentence)
            sentence = re.sub(" +", " ", sentence)
            sentence = sentence.strip()
            sentence = sentence.capitalize()

            # sentence = re.sub(word, "<b>" + word + "</b>", sentence)

            temp['sentence'] = sentence
            temp['word'] = word
            temp['translation'] = data["context"]["phrase"]["mTranslations"]["1"]
            temp['video_title'] = data["context"]["phrase"]["reference"]["title"]
            temp['date_created'] = data["timeModified_ms"]
            temp['video_id'] = data["context"]["phrase"]["reference"]["movieId"]
            temp['source'] = data["context"]["phrase"]["reference"]["source"]
            temp['image'] = data["context"]["phrase"]["thumb_next"]["dataURL"]
            temp['audio'] = data["audio"]["dataURL"]
            temp['word_trans_arr'] = data["wordTranslationsArr"]
            # temp['tag'] = data["tags"]["0"]
            
            words.append(temp.copy())
            
        load(words)
        print("end transform")

    except Exception as e:
        print('ERROR transform', str(e))

def load(words):
    try:
        if db.is_connected():
            print("Success connected to database")
        
        print("load data")
        matched = check_matched_word(words)

        print("stores data to anki")
        for word in words:
            for new in matched:
                if word["word"] == new:
                    record = get_word(word["word"])
                    if record == 0:
                        store_word(word)
                        # anki_store(word)


    except Exception as e:
        print("ERROR Load", str(e))
    
def job():
    print("workers start")

try:
    db = connection()
    anki_conn()
    extract()
    print("successfully!")
except Exception as e:
    print(str(e))

# schedule.every(1).minutes.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)