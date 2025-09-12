from my_server import app
from datetime import datetime

@app.template_filter("timestamp_to_datetime")
def timestamp_to_datetime(unix_time):
    return datetime.fromtimestamp(int(unix_time)).strftime('%Y-%m-%d %H:%M')