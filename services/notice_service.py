import json

from clients.source_registry import get_source_handler
from clients.telegram_client import send_message


def load_seen_notices():

    with open(
            "data/seen_notices.json",
            "r"
    ) as file:

        return json.load(file)


def save_seen_notices(data):

    with open(
            "data/seen_notices.json",
            "w"
    ) as file:

        json.dump(
            data,
            file,
            indent=2
        )


def process_source(
        source,
        seen_data,
        run_mode
):

    source_name = source["name"]

    handler = get_source_handler(
        source["client"]
    )

    notices = handler(
        source["url"]
    )

    seen_ids = set(
        seen_data.get(
            source_name,
            []
        )
    )

    current_ids = set()
    new_notices = []

    for notice in notices:

        notice_id = notice["id"]

        current_ids.add(
            notice_id
        )

        if run_mode == "test":

            new_notices.append(
                notice
            )

        else:

            if notice_id not in seen_ids:

                new_notices.append(
                    notice
                )

    if new_notices:

        message = (
            f"🚨 {source_name} NEW NOTICES\n\n"
        )

        for index, notice in enumerate(
                new_notices,
                start=1
        ):

            message += (
                f"{index}. {notice['title']}\n"
                f"📅 {notice['date']}\n"
            )

            if notice["url"]:

                message += (
                    f"📄 {notice['url']}\n"
                )

            message += "\n"

        send_message(
            message
        )

    if run_mode != "test":

        seen_data[source_name] = list(
            current_ids
        )

        save_seen_notices(
            seen_data
        )