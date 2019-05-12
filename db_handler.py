import pandas as pd
import uuid
import base64
import numpy as np
import signal
import sys
import scipy
import scipy.misc
from scipy.spatial import distance
np.random.seed(0)
users_csv_path = "/home/ubuntu/data/csvs/users.csv"
celebs_csv_path = "/home/ubuntu/data/csvs/celebs.csv"
preference_vector_path = "/home/ubuntu/data/users/preferences.npy"
celeba_vector_path = "/home/ubuntu/data/celebs/features.npy"
user_vector_path = "/home/ubuntu/data/users/features.npy"
celeba_imgs_path = "/home/ubuntu/data/celebs/imgs/"
users_imgs_path = "/home/ubuntu/data/users/imgs/"

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
    np.save(preference_vector_path, preference_vector)
    np.save(celeba_imgs_path, celeba_vector)
    np.save(users_imgs_path, user_vector)
    print("Data saved!")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
# signal.pause()


def add_user(user):
    global users_csv, preference_vector, user_vector
    uid = str(uuid.uuid4())

    email, first_name, gender, last_name, pref_gender, photo = user["email"], user["first_name"], user["gender"], user[
        "last_name"], user["pref"], base64_to_arr(user["photo"])
    scipy.misc.imsave(users_imgs_path + uid + '.jpg', photo)
    idx = user_vector.shape[0]
    pref_idx = preference_vector.shape[0]

    preference_vector = np.stack([preference_vector, init_user_vector.reshape(1, 128)], axis=0)
    user_vector = np.stack([user_vector, get_photo_vector(uid)], axis=0)

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


def cos_cdist(vector, matrix):
    """
    Compute the cosine distances between each row of matrix and vector.
    """
    vector = vector.reshape(1, -1)
    return scipy.spatial.distance.cdist(matrix, vector, 'cosine').reshape(-1)


def get_img(user_id):
    found = users_csv[users_csv.user_id == user_id]

    p_gender = found['pref_gender']

    p_idx = found['pref_idx']
    p_vector = preference_vector[p_idx]

    if p_gender != 2:
        interested_celeb_idxs = celebs_csv[celebs_csv.gender == p_gender].idx.reset_index(drop=True)
    else:
        interested_celeb_idxs = celebs_csv.idx.reset_index(drop=True)
    interested_celeb_vectors = celeba_vector[interested_celeb_idxs]

    cosine_distance = cos_cdist(p_vector, interested_celeb_vectors)
    idxs = np.argsort(cosine_distance)

    selected = np.random.choice(idxs[-100:], 6, replace=False)
    interested_celeb_idxs = list(interested_celeb_idxs[selected])
    celeba_data = celebs_csv.iloc[interested_celeb_idxs, :]
    output = []
    for i, row in celeba_data.iterrows():
        with open('{}{}.jpg'.format(celeba_imgs_path, row['face_id']), 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read())
        output.append({
            'photo': encoded_string,
            'id': row['face_id']
        })
    return {
        'images': output
    }


def init_user_vector(count=10):
    idx = np.arange(0, celeba_vector.shape[0])
    choiced = np.random.choice(idx, count, replace=False)
    return celeba_vector[choiced].mean()


def get_photo_vector(uid):
    pass


print("Import finished!")
