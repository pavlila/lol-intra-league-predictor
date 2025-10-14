import os
import sys
import argparse

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)

from manager import scrape_many, load_tournaments_from_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", type=str)
    args = parser.parse_args()

    if not args.list:
        print("need --list tournaments.txt")
        return 
    tournaments = load_tournaments_from_file(args.list)
    scrape_many(tournaments)

if __name__ == "__main__":
    main()