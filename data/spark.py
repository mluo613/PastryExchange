from pyspark import SparkContext

# define function combos:
def combos(somelist):
    combos = []
    user_id = somelist[0]
    for item1 in somelist[1]:
        for item2 in somelist[1]:
            if (item1 != item2) and (item2>item1):
                pairs.append(((user_id), (item1, item2)))
    return combos

sc = SparkContext("spark://spark-master:7077", "PopularItems")

# 1. Read data in as pairs of (user_id, item_id clicked on by the user)
data = sc.textFile("/tmp/data/access.log", 2)     # each worker loads a piece of the data file
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

# output file??
db = MySQLdb.connect("db", "www", "$3cureUS", "cs4501")
cursor = db.cursor()
sql2 = "Truncate table reccomendations"

cursor.execute(sql2)
db.commit()

for pair, count in output:
    cursor.execute("""INSERT INTO recommendations (item_id, recommended_items) VALUES (%s, %s) ON DUPLICATE KEY UPDATE """, (str(count), page_id[0], page_id[1]))
    print ("pair %s count %d" % (pair, count))
print ("Pair frequency counted.")

sc.stop()

