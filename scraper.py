import os
from kindle import read_clippings

DATA_FILE = 'highlights.txt'
UPLOAD_FOLDER = './data/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

clippings = read_clippings(UPLOAD_FOLDER + DATA_FILE)

import ipdb; ipdb.set_trace()

