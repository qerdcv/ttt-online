import asyncio
import os

import asyncpg


def main():
    print('Waiting for database...')
    while True:
        try:
            asyncio.run(asyncpg.connect(os.environ['DB_URI']))
        except Exception as e:
            print('Connecting', e)
            continue
        else:
            print('Database is up!')
            return


if __name__ == '__main__':
    main()
