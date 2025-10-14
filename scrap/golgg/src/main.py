import argparse
from src.manager import scrape_many, load_tournaments_from_file

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