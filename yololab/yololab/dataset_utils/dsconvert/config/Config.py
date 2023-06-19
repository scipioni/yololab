import argparse as Argparse

from ..util.PathUtil import fixPath


class Config:
    def __init__(self):
        parser = Argparse.ArgumentParser()
        parser.add_argument('--sdir', type=str, required=True)
        parser.add_argument('--ddir', type=str, required=True)
        parser.add_argument('--iw', type=str, required=True)
        parser.add_argument('--ow', type=str, required=True)
        args = parser.parse_args()
        self.__sdir = fixPath(args.sdir)
        self.__ddir = fixPath(args.ddir)
        self.__iw = args.iw
        self.__ow = args.ow

    def sourceDirectory(self):
        return self.__sdir

    def destinationDirectory(self):
        return self.__ddir

    def inputWrapper(self):
        return self.__iw

    def outputWrapper(self):
        return self.__ow
