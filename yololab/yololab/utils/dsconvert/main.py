from .config.Config import Config
from .api.DatasetConverterAPI import DatasetConverterAPI


def main():
    c = Config()
    api = DatasetConverterAPI()
    api.convert(c.sourceDirectory(), c.destinationDirectory(), c.inputWrapper(), c.outputWrapper())


if __name__ == "__main__":
    main()