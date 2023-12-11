from faker import Faker

DATASET_SIZE = 7000

datasource = Faker('zh_CN')


def generate_random_canndidate_info():
    ret_info = {}

    profile = datasource.profile()

    ret_info["name"] = profile["name"]
    ret_info["sex"] = profile["sex"]

