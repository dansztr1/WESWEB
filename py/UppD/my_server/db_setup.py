from dbhandler import create_connection

conn = create_connection()

cur = conn.cursor()
cur.execute('CREATE TABLE "worm" ("id" INTEGER, "name" TEXT, "length" INTEGER,PRIMARY KEY("id" AUTOINCREMENT) );')
cur.execute('CREATE TABLE "tree" ("id" INTEGER, "height" INTEGER,PRIMARY KEY("id" AUTOINCREMENT));')
cur.execute('CREATE TABLE "apple" ("id" INTEGER, "colour" TEXT, "tree_id" INTEGER,PRIMARY KEY("id" AUTOINCREMENT),FOREIGN KEY("tree_id") REFERENCES "tree"("id") );')
cur.execute('CREATE TABLE "gardener" ("id" INTEGER, "name" TEXT,PRIMARY KEY("id" AUTOINCREMENT));')
cur.execute('''
CREATE TABLE "gardening_tree" (
    "tree_id" INTEGER,
    "gardener_id" TEXT,
    FOREIGN KEY("tree_id") REFERENCES "tree"("id"),
    FOREIGN KEY("gardener_id") REFERENCES "gardener"("id")
);
''')

conn.close()