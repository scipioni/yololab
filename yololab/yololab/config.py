from typing import Any
import configargparse
import logging


def get_config(jupyter=False) -> Any:
    parser = configargparse.get_argument_parser()

    parser.add_argument("--debug", action="store_true", default=False, help="debug")
    parser.add_argument("--step", action="store_true", default=False, help="step mode")
    config = parser.parse_args()
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
        level="DEBUG" if config.debug else "INFO",
    )
    # parser.add_argument('--show', action='store_true',
    #                     default=False, help="debug image")
    # parser.add_argument('--size', type=int, default=416,
    #                     help='yolo size and motion size')
    # parser.add_argument('--max-frames', type=float, default=5,
    #                     help='max frames per second to process')
    # parser.add_argument('--keep-frames', type=float, default=5,
    #                     help='number of frames to keep')
    # parser.add_argument('--motion',
    #                     action='store_true', default=False, help="motion detect")
    # parser.add_argument('--start-delay', type=float, default=5, help="delay at start")
    return config  # .parse(jupyter=jupyter, pattern="*brain*py")
