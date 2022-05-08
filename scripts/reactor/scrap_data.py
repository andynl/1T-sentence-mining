import requests
import json
import re
import nltk
from nltk.stem import WordNetLemmatizer

from scripts.reactor.get_data_anki import Anki

url = "https://lb.dioco.io/base_items_itemsJsonExport_6"
url_dict = "https://api.dictionaryapi.dev/api/v2/entries/en/"

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

# res = requests.post(url, 
#     json=data, 
#     headers=headers,
# )
# reactor= res.json()

# lemmatizer = WordNetLemmatizer()
words = []
# reactors = []
# reactor_search = requests.get(reactor["data"]["file_path"]).json()
reactor_search = requests.get("https://storage.googleapis.com/nlle-b0128.appspot.com/userExportCache/lln_json_items_2022-5-6_772588.json").json()
for data in reactor_search:
    temp = {}
    # transform, cleansing sentence and word
    word = data["word"]["text"]
    sentence = data["context"]["phrase"]["subtitles"]["1"]
    sentence = re.sub("\n", " ", sentence)
    sentence = re.sub("-", "", sentence)
    sentence = re.sub(r'\[[^()]*\]', "", sentence)
    sentence = re.sub(" +", " ", sentence)
    sentence = sentence.strip()
    sentence = sentence.capitalize()
    # print(word + " ---> " + lemmatizer.lemmatize(word))

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
    temp['tag'] = data["tags"]["0"]
    # audio
    temp['audio'] = data["audio"]["dataURL"]
    # translation
    temp['word_trans_arr'] = data["wordTranslationsArr"]
    
    words.append(temp.copy())
    # check database dulu, then check anki, input data ke anki 

    # check from anki database, if word is already in anki, the word skipped
    # check from db, if word is already in database, the word skipped

    # get definition from dictionary
    # definition_search = requests.get(url_dict + word).json()
    # print(definition_search)

print(words)
 
# with open('definition.json', 'w') as f:
#     json.dump(definition_search, f)