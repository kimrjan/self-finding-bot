from argparse import ArgumentParser

import numpy as np

from app.src.bot import Bot
from app.src.environment import Environment
from app.src.utils import Utils


def main():
    parser = ArgumentParser()
    parser.add_argument("file", help="File with environment map")
    parser.add_argument("--pos", help="Start position of the bot", default=None, type=int, nargs=2)
    parser.add_argument("--dir", help="Start direction of the bot", default=None, type=int, nargs=2)
    parser.add_argument("--sight_range", help="Sight range of the bot", default=1, type=int)
    parser.add_argument("--wait", help="Wait time between printing steps", default=0.5, type=float)
    parser.add_argument("--print_map", help="If True map will be printed. Not recommended for large maps.", type=bool)

    args = parser.parse_args()

    env_ = Environment(Utils.load(args.file), np.array(args.pos) if args.pos is not None else None, np.array(args.dir) if args.dir is not None else None)
    bot_ = Bot(env_, args.sight_range)
    bot_.find_itself(args.print_map, args.wait)


if __name__ == "__main__":
    main()
