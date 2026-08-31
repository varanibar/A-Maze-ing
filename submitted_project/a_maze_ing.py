# Built-in modules
import sys

# Project modules
from maze_builder import build_maze
from ui.display import start_display


def main() -> None:
    if len(sys.argv) != 2:
        print("Error: Missing configuration file.", file=sys.stderr)
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        sys.exit(0)

    config_file = sys.argv[1]

    try:
        state = build_maze(config_file)
        start_display(state)
    except FileNotFoundError:
        print(f"Error: File '{config_file}' not found.", file=sys.stderr)
        sys.exit(0)
    except PermissionError:
        print("Error: Permission denied when reading"
              f" '{config_file}'.", file=sys.stderr)
        sys.exit(0)
    except ValueError as err:
        print(f"Configuration Error: {err}", file=sys.stderr)
        sys.exit(0)
    except Exception as err:
        print(f"Unexpected error: {err}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
