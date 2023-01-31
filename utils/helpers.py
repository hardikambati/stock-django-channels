import datetime

def get_request(*args: tuple):
    try:
        return args[1]
    except IndexError:
        return args[0]
    except Exception as e:
        raise e


def add_custom_time_to_date():
    curr_date = datetime.datetime.now()
    curr_date = curr_date.replace(
        hour=3,
        minute=30,
        second=0
    )
    return curr_date