import json

from services.notice_service import (
    load_seen_notices,
    process_source
)


with open(
        "data/config.json",
        "r"
) as file:

    config = json.load(file)

seen_data = load_seen_notices()

for source in config["sources"]:

    if not source["enabled"]:
        continue

    print(
        f"Processing {source['name']}..."
    )

    process_source(
        source,
        seen_data
    )

print("Done")