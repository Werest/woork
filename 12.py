import os
import sqlite3
import numpy as np
import cv2
import pickle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FCA

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
    # if num == 0:
    #     break
conn.commit()


ex = cursor.execute('''
select `blob` from n_table 
''')


video = cv2.VideoWriter('vnn9.avi', 0, 1, (800, 300))

tables = ex.fetchall()
for i in range(0, len(tables)):
    fig = pickle.loads(tables[i][0])
    canvas = FCA(fig)
    canvas.draw()
    nparr = np.array(canvas.renderer._renderer)
    frame = cv2.cvtColor(nparr, cv2.COLOR_RGB2BGR)

    video.write(frame)
cv2.destroyAllWindows()
video.release()



conn.close()

#         fi = sqlite3.Binary(pickle.dumps(fig))
#         sql = '''
#             insert into n_table (`directory`, `blob`, `name`) VALUES(?, ?, ?)
#         '''
#         cursor.execute(sql, [opa, fi, number])
#         conn.commit()