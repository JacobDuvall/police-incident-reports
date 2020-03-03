# -*- coding: utf-8 -*-
# Example main.py
import argparse

import project0


def main(url):
    # Download data
    data = project0.fetch_incidents(url)

    # Extract Data
    incidents = project0.extract_incidents(data)

    # Create Dataset
    project0.create_db()

    # Insert Data
    project0.populate_db(incidents)

    # Print Status
    status = project0.status()
    print(status)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True,
                        help="The incident summary url.")

    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
