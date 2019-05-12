import pandas as pd
import uuid
import base64
import numpy as np

data_path = "/home/ubuntu/data/csvs/users.csv"
df = pd.read_csv(data_path)

def add_user(user):
    # TODO
    return str(uuid.uuid4())

def get_user(user):
    user = df[df.email == user["email"]]
    if user.empty:
        uid = add_user(user)
    else:
        uid = user.image_id.values[0]
    return uid


def base64_to_arr(t):
    s = base64.b64encode(t)
    r = base64.decodebytes(s)
    q = np.frombuffer(r, dtype=np.float64)
    return q