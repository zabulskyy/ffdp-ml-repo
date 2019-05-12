import pandas as pd
import uuid

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
