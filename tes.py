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