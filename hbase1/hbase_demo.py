import happybase

# connection = happybase.Connection(host='lxschengdu.7766.org', port=19095)
connection = happybase.Connection(host='47.104.181.68', port=19090)
tables = connection.tables()
print(tables)
student = connection.table('lxs_item:Student')
print(student)
# student.put(b'111', {b'Grades:math': b'12', b'Grades:chemistry': b'22'})
# student.put(b'112', {b'Grades:math': b'89', b'Grades:chemistry': b'92'})
student.put(b'112', {b'Grades:math': b'89', b'Grades:chemistry': b'92', b'Grades:yuwen': b'39'})
res = student.scan(row_start=b'111', row_stop=b'115')
for i in res:
    print(i)

# student.put(b'test111', {b'hbase_test:a': b'demo1', b'hbase_test:b': b'tettttt'})

