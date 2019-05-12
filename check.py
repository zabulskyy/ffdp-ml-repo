import numpy as np
import pandas as pd


def get_img(user_id, all_data, vector, celebs, celeba_vector):
    """

    :param user_id: id of user for which we found 6 matches (from top 100) celebs
    :param all_data: csv user data (email,first_name,gender,idx,image_id,last_name,pref_idx,pref_gender)
    :param vector: users preference vector
    :param celebs: csv celebs (celeb_id, gender ...)
    :param celeba_vector: celebs preference vector

    :return: list, 6 celebs - [base64, celeb_id]
    """
    # take vector of preferences and gender preference
    found = all_data[all_data.user_id == user_id]

    p_gender = found['pref_gender']
    p_idx = found['pref_idx']

    p_vector = vector[p_idx]

    interested = celebs[celebs.gender == p_gender]


