from my_server import app
from flask import render_template, request
from my_server.dbhandler import sqlite3, create_connection



def get_worms(sort_order='asc'):
    if sort_order not in ['asc', 'desc']:
        sort_order = 'asc'
    conn = create_connection()
    cur = conn.cursor()
    query = f'''
        SELECT w.name, w.length, a.colour, t.height
        FROM worm w
        LEFT JOIN apple a ON w.apple_id = a.id
        LEFT JOIN tree t ON a.tree_id = t.id
        ORDER BY w.length {sort_order}
    '''
    cur.execute(query)
    data = cur.fetchall()
    conn.close()
    return data




@app.route('/', methods=['GET'])
def index():
    sort_order = request.args.get('sort_order', 'asc')
    worms = get_worms(sort_order)
    return render_template('worms.html', worms=worms, sort_order=sort_order)


if __name__ == '__main__':
    app.run(debug=True)
