"""Local SQLite key/value CLI compatible with the inspected reference."""
import argparse
import json
import sqlite3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', required=True)
    parser.add_argument('action', choices=['put', 'list', 'remove'])
    parser.add_argument('key', nargs='?')
    parser.add_argument('value', nargs='?')
    args = parser.parse_args()

    connection = sqlite3.connect(args.db)
    connection.execute(
        'create table if not exists items (key text primary key, value text not null)'
    )
    try:
        if args.action == 'put':
            if not args.key or args.value is None:
                print(json.dumps({'error': 'key and value required'}))
                return 2
            existing = connection.execute(
                'select value from items where key=?', (args.key,)
            ).fetchone()
            if existing and existing[0] != args.value:
                print(json.dumps({'error': 'key conflict'}))
                return 3
            connection.execute(
                'insert or ignore into items values (?,?)', (args.key, args.value)
            )
            connection.commit()
            result = {'key': args.key, 'value': args.value}
        elif args.action == 'list':
            result = [
                {'key': key, 'value': value}
                for key, value in connection.execute(
                    'select key,value from items order by key'
                )
            ]
        else:
            if not args.key:
                print(json.dumps({'error': 'key required'}))
                return 2
            deleted = connection.execute('delete from items where key=?', (args.key,))
            connection.commit()
            result = {'removed': bool(deleted.rowcount)}
        print(json.dumps(result))
        return 0
    finally:
        connection.close()


if __name__ == '__main__':
    raise SystemExit(main())
