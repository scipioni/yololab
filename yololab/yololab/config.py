from typing import Any
import configargparse
import logging


def get_config() -> Any:
    parser = configargparse.get_argument_parser()

    #parser.add_argument("--step", action="store_true", default=False, help="step mode")


    parser.add_argument("--debug", action="store_true", default=False, help="debugging mode")
    parser.add_argument(
        "--config", required=False, is_config_file=True, help="config file path"
    )
    parser.add_argument(
        "--config-save",
        required=False,
        is_write_out_config_file_arg=True,
        help="config file path",
    )

    parser.add_argument("images", nargs="*", default=[], help="list of images")
    parser.add_argument("--show", action="store_true", default=False)
    parser.add_argument("--dummy", action="store_true", default=False)
    parser.add_argument("--step", action="store_true", default=False)

    parser.add_argument("--models", default="./models", help="models repo")
    parser.add_argument("--model", default="yolov8n-pose", help="model name")
    parser.add_argument("--show-full", action="store_true", default=False, help="show all info")



    # parser.add_argument("--inference", action="store_true", default=False)
    # parser.add_argument("--nano", action="store_true", default=True)
    # parser.add_argument("--custom", action="store_true", default=False)


    # parser.add_argument("--quiet", action="store_true", default=False)
    # parser.add_argument(
    #     "--delay-start",
    #     type=int,
    #     default=0,
    #     help="add a delay at start (needed for truth brain tests)",
    # )
    # parser.add_argument("--camera-framerate", type=int, default=25)
    # parser.add_argument("--camera-cols", type=int, default=2048)
    # parser.add_argument("--camera-rows", type=int, default=1024)
    # parser.add_argument("--camera-roi-cols", type=int, default=1024)
    # parser.add_argument("--camera-roi-rows", type=int, default=512)
    # parser.add_argument("--camera-top", type=int, default=256)
    # parser.add_argument("--camera-shutter", type=float, default=1.0, help="shutter time in ms")
    # parser.add_argument(
    #     "--camera-AutoGainUpperLimit", type=float, default=23.0, help="AutoGainUpperLimit"
    # )
    # parser.add_argument(
    #     "--camera-AutoTargetBrightness",
    #     type=float,
    #     default=0.25,
    #     help="AutoTargetBrightness",
    # )
    # parser.add_argument(
    #     "--camera-AutoExposureTimeUpperLimit",
    #     type=float,
    #     default=5000,
    #     help="AutoExposureTimeUpperLimit",
    # )
    # parser.add_argument("--camera-color", action="store_true", default=False, help="")
    # parser.add_argument("--camera-native", action="store_true", default=False, help="")
    # parser.add_argument("--camera-basler", action="store_true", default=True, help="")
    # parser.add_argument("--camera-loop", action="store_true", default=False)
    # parser.add_argument("--camera-fake", default="", help="simulate camera with image")
    parser.add_argument("--camera-id", nargs="+", default=[0])
    # parser.add_argument("--camera-serial", default="")  # default="23255275")
    # parser.add_argument("--camera-flip-y", type=int, default=0, help="flip vertical")
    # parser.add_argument("--socket-port", type=int, default=5007)
    # parser.add_argument("--socket-ip", default="127.0.0.1")
    # parser.add_argument("--socket-ip-gps", default="127.0.0.1")
    # parser.add_argument("--socket-port-gps", type=int, default=5012)
    # parser.add_argument(
    #     "--gps-sync",
    #     action="store_true",
    #     default=False,
    #     help="emit GPS sync on UDP port --socket-port-gps",
    # )
    # # parser.add_argument('--socket-multicast-group', default='224.1.1.1')
    # parser.add_argument("--path", default=os.getcwd())
    # parser.add_argument("--save", action="store_true", default=False)
    # parser.add_argument("--save-path", default="/tmp")
    # parser.add_argument(
    #     "--save-encoder",
    #     default="x264enc speed-preset=7",
    #     help="h264 encoder [x264enc, omxh264enc control-rate=2 bitrate=10000000]",
    # )
    # parser.add_argument("--legacy", action="store_true", default=False, help="test legacy code")
    # parser.add_argument("--check-shm", type=int, default=30, help="check shm allocation every n frames; 0 disable check")

    config = parser.parse_args()
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
        level="DEBUG" if config.debug else "INFO",
    )

    return config