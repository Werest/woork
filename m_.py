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
