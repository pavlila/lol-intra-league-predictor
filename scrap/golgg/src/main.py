import sys
import argparse
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent

PARENT_DIR = CURRENT_DIR.parent

for d in [str(CURRENT_DIR), str(PARENT_DIR)]:
    if d not in sys.path:
        sys.path.insert(0, d)

from manager import GolManager


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", type=str)
    args = parser.parse_args()

    if not args.list:
        print("need --list tournaments.txt")
        return

    list_path = CURRENT_DIR / args.list

    manager = GolManager()
    tournaments = manager.load_tournaments_from_file(list_path)
    manager.scrape_many(tournaments)


if __name__ == "__main__":
    main()
