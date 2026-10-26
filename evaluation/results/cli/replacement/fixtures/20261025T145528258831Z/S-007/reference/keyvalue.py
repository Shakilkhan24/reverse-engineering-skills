import argparse, json, sqlite3
p=argparse.ArgumentParser()
p.add_argument('--db', required=True)
p.add_argument('action', choices=['put','list','remove'])
p.add_argument('key', nargs='?')
p.add_argument('value', nargs='?')
a=p.parse_args()
c=sqlite3.connect(a.db)
c.execute('create table if not exists items (key text primary key, value text not null)')
if a.action=='put':
    if not a.key or a.value is None:
        print(json.dumps({'error':'key and value required'})); raise SystemExit(2)
    old=c.execute('select value from items where key=?',(a.key,)).fetchone()
    if old and old[0]!=a.value:
        print(json.dumps({'error':'key conflict'})); raise SystemExit(3)
    c.execute('insert or ignore into items values (?,?)',(a.key,a.value)); c.commit()
    print(json.dumps({'key':a.key,'value':a.value}))
elif a.action=='list':
    print(json.dumps([{'key':k,'value':v} for k,v in c.execute('select key,value from items order by key')]))
else:
    if not a.key:
        print(json.dumps({'error':'key required'})); raise SystemExit(2)
    cur=c.execute('delete from items where key=?',(a.key,)); c.commit()
    print(json.dumps({'removed':bool(cur.rowcount)}))
