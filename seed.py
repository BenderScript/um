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
    """Initializes sqlite3"""

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
        raise SystemExit(er)


def get_list_of_users(total_users):
    """Get List of GitHub Users."""

    users = {}

    try:
        r = requests.get('https://api.github.com/users', headers={'Accept': 'application/vnd.github.v3+json'})
        users = r.json()
        len_users = len(users)
        # login, id, avatar_url, type, html_url
        while 'next' in r.links.keys() and len_users < total_users:
            resp = requests.get(r.links['next']['url'], headers={'Accept': 'application/vnd.github.v3+json'})
            more_users = resp.json()
            len_users += len(more_users)
            # Remove this break
            break
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def main():
    parser = argparse.ArgumentParser(description='Fetch GitHub Users')
    parser.add_argument('--total', type=int,
                        help='total number of users to retrieve', default=150)
    args = parser.parse_args()
    if args.total > 1000 or args.total < 1:
        print("Are you a bot? Exiting...")
        sys.exit(2)
    init_db()
    get_list_of_users(args.total)


if __name__ == "__main__":
    main()
