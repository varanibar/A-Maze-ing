# Built-in modules
from dataclasses import dataclass

# Project modules
from parser import Config, parse_config
from mazegen import MazeGenerator


@dataclass
class MazeState:
    """Store the current maze, its configuration, and rendered form."""

    config_file: str
    config_data: Config
    maze_string: str
    generator: MazeGenerator
    reserved_cells: set[tuple[int, int]]
    solver: object
    maze: object


def write_output_file(
    file_path: str,
    hex_grid: str,
    maze_entry: tuple[int, int],
    maze_exit: tuple[int, int],
    path: str,
) -> None:
    """Write the generated maze data and solution path to the output file."""
    lines = [
        hex_grid,
        "",
        f"{maze_entry[0]},{maze_entry[1]}",
        f"{maze_exit[0]},{maze_exit[1]}",
        path,
    ]

    with open(file_path, "w") as file:
        file.write("\n".join(lines))


def build_maze(config_file: str) -> MazeState:
    """Parse configuration, generate a maze using MazeGenerator,
    and save output."""
    config_data = parse_config(config_file)

    generator = MazeGenerator(
        width=config_data.width,
        height=config_data.height,
        maze_entry=config_data.maze_entry,
        maze_exit=config_data.maze_exit,
        seed=config_data.seed,
        perfect=config_data.perfect,
    )

    generator.generate()

    write_output_file(
        file_path=config_data.output_file,
        hex_grid=generator.to_hex_grid(),
        maze_entry=config_data.maze_entry,
        maze_exit=config_data.maze_exit,
        path=generator.get_solution(),
    )

    return MazeState(
        config_file=config_file,
        config_data=config_data,
        maze_string=generator.render(),
        generator=generator,
        reserved_cells=generator.reserved_cells,
        solver=generator.solver,
        maze=generator.maze,
    )


def regenerate_maze(state: MazeState) -> MazeState:
    """Regenerate a new maze using the stored configuration file."""
    return build_maze(state.config_file)
