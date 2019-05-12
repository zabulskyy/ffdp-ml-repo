import pandas as pd
import uuid
import base64
import numpy as np
import signal
import sys

data_path = "/home/ubuntu/data/csvs/users.csv"
# email,first_name,gender,idx,user_id,last_name,pref_idx,pref_gender
print("Reading database..")
df = pd.read_csv(data_path)
print("Done!")

#
# def signal_handler(sig, frame):
#     print("Interruption!")
#     df.to_csv(data_path)
#     sys.exit(0)
#
#
# signal.signal(signal.SIGINT, signal_handler)
# # signal.pause()


def add_user(user):
    global df
    uid = str(uuid.uuid4())
    idx = max(df.idx) + 1
    pref_idx = -1
    email, first_name, gender, last_name, pref_gender = user["email"], user["first_name"], user["gender"], user[
        "last_name"], user["pref"]
    new_data_record = pd.DataFrame([[idx,email, first_name, gender, idx, uid, last_name, pref_idx, pref_gender]],
                                   columns=df.columns)
    df = df.append(new_data_record)
    return uid


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


print("Import finished!")
