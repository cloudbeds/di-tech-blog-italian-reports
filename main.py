import pprint

import requests

# Data Insights API
BASE_URL = "https://api.cloudbeds.com/datainsights"

# TODO: populate with your propert ID and authorization token
YOUR_PROPERTY_ID = 0  # ID of your property
YOUR_AUTH_TOKEN = ""  # Your authorization code

# The three reports needed for the Italian Statistics Report
GUEST_INFO_REPORT = {
    "property_ids": [
        YOUR_PROPERTY_ID,
    ],
    "dataset_id": 2,
    "filters": {
        "and": [
            {
                "cdf": {"type": "default", "column": "checkin_date"},
                "value": "yesterday",
                "operator": "greater_than_or_equal",
            }
        ]
    },
    "columns": [
        {"cdf": {"column": "italian_guest_type"}},
        {"cdf": {"column": "checkin_date"}},
        {"cdf": {"column": "guest_surname"}},
        {"cdf": {"column": "guest_first_name"}},
        {"cdf": {"column": "guest_gender"}},
        {"cdf": {"column": "guest_birth_date"}},
        {"cdf": {"column": "italian_guest_birth_date_municipality_code"}},
        {"cdf": {"column": "italian_guest_birth_date_province_code"}},
        {"cdf": {"column": "italian_guest_birth_country_code"}},
        {"cdf": {"column": "italian_guest_nationality_code"}},
        {"cdf": {"column": "guest_city"}},
        {"cdf": {"column": "guest_state"}},
        {"cdf": {"column": "guest_residence_country"}},
        {"cdf": {"column": "guest_address"}},
        {"cdf": {"column": "guest_document_type"}},
        {"cdf": {"column": "guest_document_number"}},
        {"cdf": {"column": "italian_guest_document_issuing_province_code"}},
        {"cdf": {"column": "italian_guest_document_issuing_municipality_code"}},
        {"cdf": {"column": "guest_document_issuing_country_code"}},
        {"cdf": {"column": "checkout_date"}},
    ],
    "settings": {"details": True, "totals": False, "transpose": False},
}
OCCUPIED_ROOMS = {
    "property_ids": [22425],
    "dataset_id": 4,
    "filters": {
        "and": [
            {
                "value": "2023-02-01T00:00:00.000Z",
                "cdf": {"type": "default", "column": "stay_date"},
                "operator": "greater_than_or_equal",
            },
            {
                "value": "2023-02-28T00:00:00.000Z",
                "cdf": {"type": "default", "column": "stay_date"},
                "operator": "less_than_or_equal",
            },
        ]
    },
    "columns": [{"cdf": {"column": "booking_qty_type_a"}, "metrics": ["sum"]}],
    "settings": {"totals": False, "details": False},
    "group_rows": [{"cdf": {"column": "stay_date"}, "modifier": "day"}],
    "custom_cdfs": [],
}
UNOCCUPIED_ROOMS = {
    "property_ids": [
        YOUR_PROPERTY_ID,
    ],
    "dataset_id": 4,
    "filters": {
        "and": [
            {
                "value": "2023-02-01T00:00:00.000Z",
                "cdf": {"type": "default", "column": "stay_date"},
                "operator": "greater_than_or_equal",
            },
            {
                "value": "2023-02-28T00:00:00.000Z",
                "cdf": {"type": "default", "column": "stay_date"},
                "operator": "less_than_or_equal",
            },
            {
                "value": "0",
                "cdf": {"type": "default", "column": "booking_qty_type_a"},
                "operator": "equals",
            },
        ]
    },
    "columns": [
        {"cdf": {"column": "room_available_type_a"}, "metrics": ["sum"]},
        {"cdf": {"column": "bed_based_capacity"}, "metrics": ["sum"]},
    ],
    "settings": {"totals": False, "details": False},
    "group_rows": [{"cdf": {"column": "stay_date"}, "modifier": "day"}],
    "custom_cdfs": [],
}


if __name__ == "__main__":
    # Set up the pretty printer
    printer = pprint.PrettyPrinter(indent=4)

    # Required Headers
    headers = {
        "ACCEPT-LANGUAGE": "en",
        "X-PROPERTY-ID": str(YOUR_PROPERTY_ID),
        "Authorization": f"Bearer {YOUR_AUTH_TOKEN}",
    }

    # Get Datasets
    datasets_response = requests.get(
        "https://api.cloudbeds.com/datainsights/v1.1/datasets", headers=headers
    )
    for dataset in datasets_response.json():
        print(f"ID: {dataset['id']}, Name: {dataset['name']}")

    # Get Cloudbeds Data Fields (CDFs)
    dataset_cdfs_response = requests.get(
        "https://api.cloudbeds.com/datainsights/v1.1/datasets/1", headers=headers
    )
    for category in dataset_cdfs_response.json()["cdfs"]:
        print(f"Category: {category['category']}")
        for cdf in category["cdfs"]:
            print(
                f"Cloudbeds Data Field Name: {cdf['name']}, Cloudbeds Data Column: {cdf['column']}"
            )

    # Query parameters for the "query data" request
    query_params = dict(
        mode="Run",  # Other option is "Preview", which limits the result to 100 records
    )

    # Query the Guest Information report
    print("Querying the Guest Information data...")
    report_query_response = requests.post(
        "https://api.cloudbeds.com/datainsights/v1.1/reports/query/data",
        params=query_params,
        headers=headers,
        json=GUEST_INFO_REPORT,
    )
    printer.pprint(report_query_response.json())

    # Query the Occupied Rooms report
    print("Querying the Occupied Rooms data...")
    report_query_response = requests.post(
        "https://api.cloudbeds.com/datainsights/v1.1/reports/query/data",
        params=query_params,
        headers=headers,
        json=OCCUPIED_ROOMS,
    )
    printer.pprint(report_query_response.json())

    # Query the Unoccupied Rooms report
    print("Querying the Unoccupied Rooms data...")
    report_query_response = requests.post(
        "https://api.cloudbeds.com/datainsights/v1.1/reports/query/data",
        params=query_params,
        headers=headers,
        json=UNOCCUPIED_ROOMS,
    )
    printer.pprint(report_query_response.json())
