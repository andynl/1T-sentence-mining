import mysql.connector
import uuid

def connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            port="3307",
            database="sentence_mining_db"
        )

        return db
    except Exception as e:
        print('Connection Error', str(e))
    
def get_word(word):
    try:
        db = connection()
        cursor = db.cursor(buffered=True)
        sql = "SELECT * FROM words WHERE word = %s"
        values = [
            (word)
        ]
        cursor.execute(sql, values)
        record = cursor.rowcount
        cursor.close()
        return record
    except Exception as e:
        print('Get Word Error', str(e))

def store_word(word):
    try:
        db = connection()
        cursor = db.cursor(buffered=True)
        sql = """INSERT INTO words (item_key, subtitle, word, definition, trans, video_id, video_title, date_created, source, image, type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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

        for val in values:
            cursor.execute(sql, val)
            db.commit()
        
        cursor.close()
    except Exception as e:
        print('Store Word Error', str(e))
    
# CREATE TABLE `words` (
# 	id INT PRIMARY KEY AUTO_INCREMENT,
# 	item_key varchar(255), 
# 	subtitle varchar(255), 
# 	word varchar(255), 
# 	definition varchar(255),
# 	trans varchar(255), 
# 	video_id varchar(255), 
# 	video_title varchar(255), 
# 	date_created varchar(255), 
# 	source varchar(255), 
# 	image BLOB,
# 	type varchar(20),
# 	created_at timestamp
# ) ENGINE = InnoDB;