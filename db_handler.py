import pandas as pd
import uuid
import base64
import numpy as np
import signal
import sys


users_csv_path = "/home/ubuntu/data/csvs/users.csv"
celebs_csv_path = "/home/ubuntu/data/csvs/celebs.csv"
preference_vector_path = "/home/ubuntu/data/users/preferences.npy"
celeba_vector_path = "/home/ubuntu/data/celebs/features.npy"
user_vector_path = "/home/ubuntu/data/users/features.npy"

# email,first_name,gender,idx,user_id,last_name,pref_idx,pref_gender
print("Reading database..")
users_csv = pd.read_csv(users_csv_path)
celebs_csv = pd.read_csv(celebs_csv_path)
preference_vector = np.load(preference_vector_path)
celeba_vector = np.load(celeba_vector_path)
user_vector = np.load(user_vector_path)
print("Done!")

def signal_handler(sig, frame):
    print("Interruption!")
    users_csv.to_csv(users_csv_path, index=False)
    celebs_csv.to_csv(celebs_csv_path, index=False)
    print("Data saved!")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
# signal.pause()


def add_user(user):
    global users_csv
    uid = str(uuid.uuid4())
    idx = max(users_csv.idx) + 1
    pref_idx = -1
    email, first_name, gender, last_name, pref_gender = user["email"], user["first_name"], user["gender"], user[
        "last_name"], user["pref"]
    new_data_record = pd.DataFrame([[idx,email, first_name, gender, idx, uid, last_name, pref_idx, pref_gender]],
                                   columns=users_csv.columns)
    users_csv = users_csv.append(new_data_record)
    return uid


def get_user(user):
    db_user = users_csv[users_csv.email == user["email"]]
    if db_user.empty:
        uid = add_user(user)
    else:
        uid = db_user.image_id.values[0]
    return uid


def base64_to_arr(t):
    s = base64.b64encode(t)
    r = base64.decodebytes(s)
    q = np.frombuffer(r, dtype=np.float64)
    return q


def get_img(user_id):
    """

    :param user_id: id of user for which we found 6 matches (from top 100) celebs
    :param all_data: csv user data (email,first_name,gender,idx,image_id,last_name,pref_idx,pref_gender)
    :param vector: users preference vector
    :param celebs: csv celebs (celeb_id, gender ...)
    :param celeba_vector: celebs preference vector

    :return: list, 6 celebs - [base64, celeb_id]
    """
    # take vector of preferences and gender preference
    found = users_csv[users_csv.user_id == user_id]

    p_gender = found['pref_gender']
    p_idx = found['pref_idx']

    p_vector = preference_vector[p_idx]

    if(p_gender != 2):
        interested = celebs_csv[celebs_csv.gender == p_gender]
    else:
        interested = celebs_csv

print("Import finished!")
