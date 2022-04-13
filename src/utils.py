from xml.dom.minidom import ReadOnlySequentialNamedNodeMap

from requests import delete
from main import all_albums
from src import db_managing
from src import JSONconverter


#grab only first/second element of item in array
def getRequiredId(list, order):
    if order == 1 or order == 0:
      required_id = []
      order_item = order
      for item in list:
        required_id.append(item[order_item])
      return required_id

