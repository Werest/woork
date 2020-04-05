import pymysql

connection = pymysql.connect(host='localhost',
                             user='newuser',
                             password='password',
                             db='dbo',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


def write_file(data):
    # Convert binary data to proper format and write it on Hard Disk
    with open('9900.png', 'wb') as file:
        file.write(data)


def sql(id):
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "call get_File(16);"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            for filee in result:
                write_file(filee['file'])
    finally:
        connection.close()


sql(16)


def sql():
    try:
        with connection.cursor() as cursor:
            sql = "call dbo.get_File();"
            cursor.execute(sql)
            result = cursor.fetchall()
            for j, res in enumerate(result):
                file = 'konstantin' + result[j]['name_file']
                if os.path.exists(file):
                    sp = file.split('/')
                    for i, k in enumerate(sp[:-1]):
                        sp[i] = sp[i] + '_'
                    name_finally = ''.join(sp[1:])
                    image = color.rgb2gray(io.imread(file))
                    image = cv2.blur(image, (3, 3))

    finally:
        connection.close()
