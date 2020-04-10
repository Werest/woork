import os
import sqlite3
import numpy as np
import cv2

directory = "2020-2/A4 98 um 20200325/"
ddd = "k1"
# https://docs.python.org/3/library/sqlite3.html

conn = sqlite3.connect('i.db')

cursor = conn.cursor()
sql = '''
    create table if not exists n_table(
	    id integer primary key,
	    path text not null,
	    blob blob not null)
	'''
cursor.execute(sql)


sql = '''
    insert into n_table (`directory`, `blob`, `name`) VALUES(?, ?, ?)
'''
# cursor.execute(sql, [directory, ry, '0.png'])

remove_ds_store = [name for name in os.listdir(ddd) if not name.startswith(('.', 'ORG'))]
sort_list = sorted(remove_ds_store)
for num, path in enumerate(sort_list):
    path1 = ddd + '/' + path
    with open(path1, 'rb') as foo:
        l = foo.read()
    foo.close()
    ry = sqlite3.Binary(l)
    # cursor.execute(sql, [ddd, ry, path])
conn.commit()


ex = cursor.execute('''
select `blob` from n_table
''')

jk = ex.fetchone()


nparr = np.fromstring(jk[0], np.uint8)
frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
height, width, layers = frame.shape
video = cv2.VideoWriter('vnn.avi', 0, 1, (width, height))

ha = ex.fetchall()

for num, blob in enumerate(ha):
    for b in blob:
        nparr = np.fromstring(b, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        video.write(frame)
cv2.destroyAllWindows()
video.release()

conn.close()