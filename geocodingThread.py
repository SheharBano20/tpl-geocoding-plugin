import requests
from PyQt5.QtCore import QThread, pyqtSignal
from base64 import b64encode
from threading import *
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from . import Configuration as conf

class Geocoding(QThread):

    rows = pyqtSignal(object)
    error = pyqtSignal(object)
    vals = pyqtSignal(object)

    def __init__(self, fn_to_run, api, raw_address):
    # def __init__(self, fn_to_run, result,api, other_options, options, Offset, Limit, Polygon, Radius,Point,Searchtype, apikey):
        QThread.__init__(self)
        self.fn_to_run = fn_to_run
        self.raw_address = raw_address
        self.resp = api
        # self.result = result
        # self.api = api
        # self.other_options = other_options
        # self.options = options
        # self.offset = Offset
        # self.Limit = Limit
        # self.Polygon = Polygon
        # self.Radius = Radius
        # self.Point = Point
        # self.Searchtype = Searchtype
        # self.apikey = apikey
        self.threadactive = True


    def __del__(self):
         self.threadactive = False
         self.wait()

    def createAPI(self):
        try:
                # print(resp)
                # self.vals.emit(resp)
                count  = 0
                session = requests.Session()
                retry = Retry(connect=3, backoff_factor=0.5)
                adapter = HTTPAdapter(max_retries=retry)
                session.mount('http://', adapter)
                session.mount('https://', adapter)

                val = session.get(self.resp.encode('utf-8')).json()
                status = session.get(self.resp).status_code
                lng = 0.0
                lat = 0.0
                precision = ''
                compound_address_parents = ''
                remarks = ''
                subcategory = ''
                category = ''
                name = ''
                priority = ''
                if status == 200:
                    try:
                        if (val.get('data')):
                            compound_address_parents = val['data'][0]['compound_address_parents']
                            lng = val['data'][0]['lng']
                            lat = val['data'][0]['lat']
                            precision = val['metadata']['precision']
                            remarks = status
                            subcategory = val['data'][0]['subcat_name']
                            category = val['data'][0]['cat_name']
                            name = val['data'][0]['name']
                            priority = val['data'][0]['priority']

                        else:
                            count = count + 1
                            precision = val['metadata']['precision']
                            remarks = str(status)


                    except Exception as e:
                        count = count + 1
                        precision = 'not precise'
                        remarks = str(status)
                        # self.error.emit(e)
                else:
                    precision = 'not precise'
                    remarks = str(status)
                    count = count + 1
                    pass


                self.api_result = {'raw_address': self.raw_address,'Lat': lat, 'Long': lng, 'Geocoded Address': compound_address_parents,
                                   'Precision': precision, 'Subcategory': subcategory,
                                   'Category': category, 'Name': name, 'Priority': priority,
                                   'Remarks': remarks, 'Count':count}
                self.rows.emit(self.api_result)
                # self.processEvents()
        except Exception as e:
            self.error.emit(e)

    def run(self):
        # self.vals()
        if self.fn_to_run == 'geocode':
            self.createAPI()
            # self.createAPI(self.result,self.api, self.other_options, self.options,self.Offset, self.Limit, self.Polygon, self.Radius,self.Point,self.Searchtype, self.apikey)


