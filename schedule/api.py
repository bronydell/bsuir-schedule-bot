import requests
from json import JSONDecodeError

BASE_API_PATH = "https://students.bsuir.by/api/v1/"


def get_api_path(method):
    return '{api_path}/{method}'.format(api_path=BASE_API_PATH, method=method)


def get_schedule(student_group):
    try:
        path = get_api_path('studentGroup/schedule')
        response = requests.get(path, params={
            "studentGroup": student_group,
        })

        return response.json()
    except JSONDecodeError:
        raise Exception("No schedule for that group or something went wrong")

