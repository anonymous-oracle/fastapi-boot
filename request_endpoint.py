######################### HEADERS ##################################
# REQUEST_TYPE: {ENRL, INFR, RENRL}
# GROUP_ID: <group-id>
####################################################################

####### CODES FOR REQUEST_TYPE #######
# ENRL: for enrollment request
# INFR: for inference request
# RENRL: for re-enrollment request
######################################

############## USAGE ##################
# $0: <URL> <FILEPATH> <REQUEST_TYPE> <GROUP_ID>
######################################


import requests
import sys
from time import perf_counter

URL = sys.argv[1]
# URL = 'http://127.0.0.1:5000/enroll'

FILEPATH = sys.argv[2]
REQUEST_TYPE = sys.argv[3]

GROUP_ID = sys.argv[4]
# GROUP_ID = 'rev-speaker'


headers = {'REQUEST_TYPE': REQUEST_TYPE, 'GROUP_ID': GROUP_ID}

files = {"file": (FILEPATH, open(FILEPATH, 'rb'))}
t = perf_counter()
r = requests.post(URL, files=files, headers=headers)
time_elapsed = perf_counter() - t
print(f"TIME ELAPSED: {time_elapsed}")
print(r.json())
