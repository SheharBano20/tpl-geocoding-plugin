import requests
from PyQt5.QtCore import QThread, pyqtSignal
from base64 import b64encode
from threading import *
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from .dbConfiguration import DbConfig
from . import Configuration as conf

class FetchResult(QThread):

    rows = pyqtSignal(object)
    error = pyqtSignal(object)

    def __init__(self, fn_to_run, query):

        QThread.__init__(self)
        self.fn_to_run = fn_to_run
        self.query = query
        self.threadactive = True


    def __del__(self):
        self.threadactive = False
        self.wait()

    def fetch_results(self):
        try:
                db = DbConfig('172.16.130.23', 'TPLMaps', '5432', 'shehar.bano', 'shehar123')
                conn = db.ConnectDb()
                result = db.DbResultsQuery(self.query)
                self.rows.emit(result)
        except Exception as e:
            self.error.emit(e)

    def run(self):
        if self.fn_to_run == 'fetch':
            self.fetch_results()


