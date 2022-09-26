import datetime
import time
import pandas as pd

class Datamanage :
    def __init__(self):
        self.data = {
            'time' : [],
            'focus_prob' : [],
            'focus' : []
        }