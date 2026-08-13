import random
from dataclasses import dataclass
from parser import parse_config
from parser import Config
from mazegen.maze import Maze
from mazegen.generator import MazeGenerator


@dataclass
class MazeState:
    config_file: str
    config_data: Config
    maze_string: str


def build_maze(config_file: str) -> MazeState:

    try:

        config_data = parse_config(config_file)

        if config_data.seed is not None:
            random.seed(config_data.seed)

        grid = Maze(config_data.width, config_data.height)
        builder = MazeGenerator(
            grid, (config_data.maze_entry[0], config_data.maze_entry[1])
        )

        builder.generate()

        if not config_data.perfect:
            builder.make_imperfect()

        maze_string = grid.render()

        return MazeState(
                config_file=config_file,
                config_data=config_data,
                maze_string=maze_string
                )

    except Exception as err:
        raise Exception(f"Maze generation - {err.__class__.__name__}: {err}")
