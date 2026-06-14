from clients.ssc_client import get_latest_notices
from clients.ibps_client import fetch_notices


def get_source_handler(client_name):

    handlers = {
        "ssc": get_latest_notices,
        "ibps": fetch_notices
    }

    if client_name not in handlers:
        raise Exception(
            f"Unsupported client: {client_name}"
        )

    return handlers[client_name]