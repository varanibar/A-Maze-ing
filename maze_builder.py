import random
from parser import parse_config
from parser import Config
from mazegen.maze import Maze
from mazegen.generator import MazeGenerator


def build_maze(config_file: str) -> tuple[Config, str]:

    try:
        config_data = parse_config("config.txt")

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
   
        return (config_data, maze_string)

    except Exception as err:
        raise Exception(f"Maze generation error: {err.__class__.__name__}: {err}")
