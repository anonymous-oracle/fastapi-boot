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

# URL = sys.argv[1]
URL = "http://127.0.0.1:8000/items/5194194?q=query"

# FILEPATH = sys.argv[2]
# REQUEST_TYPE = sys.argv[3]

# GROUP_ID = sys.argv[4]
# GROUP_ID = 'rev-speaker'

# id: int
# name: str
# price: float
# tax: Optional[float] = None
# description: Optional[str] = None

# body = {
#     "id": 5194194,
#     "name": "Cookies",
#     "price": 15.99,
#     "tax": 0.99,
#     "description": "Home-made chocolate chip cookies",
# }

body = {
    "name": "Cookies",
    "price": 15.99,
    "tax": 0.99,
    "description": "Home-made chocolate chip cookies",
}

# files = {"file": (FILEPATH, open(FILEPATH, "rb"))}

# send request body data to the json argument always
r = requests.post(URL, json=body)
print(r.json())
