#!/usr/bin/env python3
import argparse
import sys

import requests
import sqlite3


# curl \
#   -H "Accept: application/vnd.github.v3+json" \
#   https://api.github.com/users
#

def init_db():
    try:
        conn = sqlite3.connect(':memory:')
        c = conn.cursor()
        # Create table
        c.execute('''CREATE TABLE users
                     (username text, id text, image text, type text, profile real)''')
        # Save (commit) the changes
        conn.commit()
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        sys.exit(2)


def get_list_of_users(num_users):
    users = {}
    r = requests.get('https://api.github.com/users', headers={'Accept': 'application/vnd.github.v3+json'})
    users = r.json()
    while 'next' in r.links.keys():
        resp = requests.get(r.links['next']['url'], headers={'Accept': 'application/vnd.github.v3+json'})
        break


def main():
    parser = argparse.ArgumentParser(description='Fetch GitHub Users')
    parser.add_argument('--total', type=int,
                        help='total number of users', default=150)
    args = parser.parse_args()
    init_db()
    get_list_of_users(args.total)


if __name__ == "__main__":
    main()
