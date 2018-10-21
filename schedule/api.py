import requests
from json import JSONDecodeError

from schedule.exceptions import NoSchedule

BASE_API_PATH = "https://journal.bsuir.by/api/v1/portal/"


def get_api_path(method):
    return '{api_path}/{method}'.format(api_path=BASE_API_PATH, method=method)


def get_schedule(student_group):
    try:
        path = get_api_path('schedule')
        response = requests.get(path, params={
            "studentGroup": student_group,
        })
        return response.json()
    except JSONDecodeError:
        raise NoSchedule("No schedule for that group or something went wrong")

