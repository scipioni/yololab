from config.Config import Config
from api.DatasetConverterAPI import DatasetConverterAPI

c = Config()
api = DatasetConverterAPI()
api.convert(c.sourceDirectory(), c.destinationDirectory(), c.inputWrapper(), c.outputWrapper())
