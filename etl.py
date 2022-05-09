import requests
import json
import re

url = "https://lb.dioco.io/base_items_itemsJsonExport_6"
url_anki_connect = 'http://localhost:8765'
deck = 'deck:Netflix'

# extract data from languange reactor
def extract():
    try:
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

    except Exception as e:
        print(str(e))

def load(words):
    try:
        matched = check_matched_word(words)

        for word in words:
            for new in matched:
                if word["word"] == new:
                    print("New word: ", new)

    except Exception as e:
        print(str(e))

def check_matched_word(words):
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
    
try:
    anki_conn()
    extract()
except Exception as e:
    print(str(e))
