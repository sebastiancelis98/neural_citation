import psycopg2
import psycopg2.extras

print('running...')

# Connect to Postgres
conn = psycopg2.connect("dbname=MAG19 user=mag password=1maG$ host=localhost port=8888")
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

print('conntected to database, running query...')

query = 'SELECT sourceurl, sourcetype FROM paperurls where paperid=59226'

cur.execute(query)

row = cur.fetchone()
url = row['sourceurl']

query = 'SELECT originaltitle, publishedyear, referencecount, citationcount, originalvenue, publisher, doctype FROM papers where paperid=59226'

cur.execute(query)

row = cur.fetchone()
print(row)

print('done')


