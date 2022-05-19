import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="sentence_mining_db"
)

if db.is_connected():
    print("Success connected to database")

cursor = db.cursor()
sql = """INSERT INTO words (item_key, subtitle, word, trans, video_id, video_title, date_created, lemma, source, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
values = [(
    123, 
    123, 
    123, 
    123, 
    123, 
    123, 
    123, 
    123, 
    123, 
    123,
)]

for val in values:
    cursor.execute(sql, val)
    db.commit()

print("Database")

# CREATE TABLE `words` (
# 	id INT PRIMARY KEY AUTO_INCREMENT,
# 	item_key varchar(50), 
# 	subtitle varchar(50), 
# 	word varchar(50), 
# 	trans varchar(50), 
# 	video_id varchar(50), 
# 	video_title varchar(50), 
# 	date_created varchar(50), 
# 	lemma varchar(50), 
# 	source varchar(20), 
# 	image BLOB
# ) ENGINE = InnoDB;