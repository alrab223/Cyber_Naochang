import sqlite3
import json
with (sqlite3.connect("bot_data.db")) as conn:
    c = conn.cursor()
    sql = c.execute(f'select id,members,reset,vc_notification from vc_notification_setting where members>0')
    id_list = [x for x in sql]
    print(id_list)
 