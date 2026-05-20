"""
Soccer Player Performance Analyzer

This program analyzes soccer player performance using match data stored in a text file.
Each line of the file contains:

    PlayerName, Goals, Assists, MinutesPlayed

The program calculates:
- Total goals and assists
- Total matches played
- Total minutes played
- Average goals per match
- Performance category (Elite, Good, Average, Poor)

The user can:
- View all players
- View top N players by goals
- Search for a player
- Save a report to a file

This program demonstrates file I/O, loops, conditions, functions,
and use of lists, tuples, and dictionaries.
"""

import sys

INPUT_FILE = "Soccer_Player_Performance_Analyzer_input.txt"
OUTPUT_FILE = "Soccer_Player_Performance_Analyzer_output.txt"

players = {}

# -------------------- FUNCTIONS --------------------

def parse_line(line):
    parts = [p.strip() for p in line.split(",")]

    if len(parts) != 4:
        raise ValueError("Invalid format")

    name = parts[0]
    goals = int(parts[1])
    assists = int(parts[2])
    minutes = int(parts[3])

    return name, goals, assists, minutes


def add_record(name, goals, assists, minutes):
    if name not in players:
        players[name] = []

    players[name].append((goals, assists, minutes))


def compute_stats(records):
    matches = len(records)
    total_goals = sum(r[0] for r in records)
    total_assists = sum(r[1] for r in records)
    total_minutes = sum(r[2] for r in records)

    avg_goals = total_goals / matches if matches > 0 else 0

    # Performance category using conditions
    if avg_goals >= 1:
        category = "Elite"
    elif avg_goals >= 0.5:
        category = "Good"
    elif avg_goals > 0:
        category = "Average"
    else:
        category = "Poor"

    return {
        "matches": matches,
        "goals": total_goals,
        "assists": total_assists,
        "minutes": total_minutes,
        "avg_goals": avg_goals,
        "category": category
    }


def build_all_stats():
    stats = {}
    for name in players:
        stats[name] = compute_stats(players[name])
    return stats


def print_player(name, stat):
    print(f"{name}: Goals={stat['goals']}, Assists={stat['assists']}, "
          f"Matches={stat['matches']}, AvgGoals={stat['avg_goals']:.2f}, "
          f"Category={stat['category']}")


def show_top_players(stats, n):
    sorted_players = sorted(stats.items(),
                            key=lambda x: x[1]["goals"],
                            reverse=True)

    print("\nTop Players by Goals:")
    for i in range(min(n, len(sorted_players))):
        name, stat = sorted_players[i]
        print(f"{i+1}. {name} - {stat['goals']} goals")


def write_report(stats):
    with open(OUTPUT_FILE, "w") as f:
        f.write("Soccer Player Report\n\n")

        for name in stats:
            stat = stats[name]
            f.write(f"{name}: Goals={stat['goals']}, Assists={stat['assists']}, "
                    f"Matches={stat['matches']}, AvgGoals={stat['avg_goals']:.2f}, "
                    f"Category={stat['category']}\n")

    print("Report saved to file.")


def load_file():
    try:
        with open(INPUT_FILE, "r") as f:
            for line in f:
                if line.strip() == "":
                    continue

                try:
                    name, g, a, m = parse_line(line)
                    add_record(name, g, a, m)
                except:
                    print("Skipping invalid line:", line.strip())

    except FileNotFoundError:
        print("Input file not found.")
        sys.exit()


def menu(stats):
    while True:
        print("\nMenu")
        print("1 - Show all players")
        print("2 - Show top players")
        print("3 - Search player")
        print("4 - Save report")
        print("5 - Quit")

        choice = input("Enter choice: ")

        if choice == "1":
            for name in stats:
                print_player(name, stats[name])

        elif choice == "2":
            try:
                n = int(input("How many players? "))
                show_top_players(stats, n)
            except:
                print("Invalid number")

        elif choice == "3":
            name = input("Enter player name: ")
            if name in stats:
                print_player(name, stats[name])
            else:
                print("Player not found")

        elif choice == "4":
            write_report(stats)

        elif choice == "5":
            print("Goodbye")
            break

        else:
            print("Invalid choice")


# -------------------- MAIN --------------------

def main():
    print("Soccer Player Analyzer")

    load_file()

    stats = build_all_stats()

    if len(stats) == 0:
        print("No data found.")
        return

    show_top_players(stats, 5)

    menu(stats)


if __name__ == "__main__":
    main()
