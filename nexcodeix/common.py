import uuid


def uuid_without_dash():
    return uuid.uuid4().hex
