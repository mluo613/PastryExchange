from pyspark import SparkContext
import MySQLdb

# define function combos:
def combos(somelist):
    combos = []
    user_id = somelist[0]
    for item1 in somelist[1]:
        for item2 in somelist[1]:
            if (item1 != item2) and (item2>item1):
                combos.append(((user_id), (item1, item2)))
    return combos

sc = SparkContext("spark://spark-master:7077", "PopularItems")

# 1. Read data in as pairs of (user_id, item_id clicked on by the user)
data = sc.textFile("/tmp/data/access_log.txt", 2)     # each worker loads a piece of the data file
#data = sc.textFile("/tmp/data/example_data.txt", 2)
initial_pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition

# 2. Group data into (user_id, list of item ids they clicked on)
group_items = initial_pairs.groupByKey()

# 3. Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
user_to_pairs = group_items.flatMap(lambda x: combos(x))

# 4. Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
pair_to_users = user_to_pairs.groupBy(lambda x: x[1])

# 5. Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
total_count = pair_to_users.map(lambda x: ((x[0]), len(x[1])) )

# 6. Filter out any results where less than 3 users co-clicked the same pair of items
filter_total = total_count.filter(lambda x: x[1] >= 3)

output = filter_total.collect()                          # bring the data back to the master node so we can print it out
f = open("output_log.txt", "a+")

#db = MySQLdb.connect("db", "www", "$3cureUS", "cs4501")
db = MySQLdb.connect(host="db", user="www", passwd="$3cureUS", db="cs4501")
cursor = db.cursor()
sql2 = "Truncate table api_recommendations"

cursor.execute(sql2)
db.commit()

for page_id, count in output:
    command = 'INSERT INTO api_recommendations (item_id_num, recommended_items) VALUES ("%s", "%s") ON DUPLICATE KEY UPDATE recommended_items= CONCAT(recommended_items, ",", "%s")'
    cursor.execute(command, (int(page_id[0]), str(page_id[1]), str(page_id[1])) )
    cursor.execute(command, (int(page_id[1]), str(page_id[0]), str(page_id[0])) )
    db.commit()
    message = str(page_id) + '\t' + str(count) + '\n'
    f.write(message)
    print ("page_id %s count %d" % (page_id, count))
f.write("Popular items done.")
print ("Popular items done.")

f.close()
db.close()
sc.stop()

