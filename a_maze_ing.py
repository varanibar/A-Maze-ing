import sys
from ui.display import start_display
from maze_builder import build_maze
from maze_builder import write_output_file


def main() -> None:
    if len(sys.argv) != 2:
        print("Error: Missing configuration file.", file=sys.stderr)
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.strerr)
        sys.exit(1)

    config_file = sys.argv[1]

    try:

        state = build_maze(config_file)

        write_output_file(
                        state.config_data.output_file,
                        state.maze,
                        state.config_data.maze_entry,
                        state.config_data.maze_exit,
                        ""
                        )

        start_display(state)

    except FileNotFoundError:
        print(f"Error: File '{config_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print("Error: Permission denied when reading"
              f" '{config_file}'.", file=sys.stderr)
        sys.exit(1)
    except ValueError as err:
        print(f"Configuration Error: {err}", file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(f"{err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
