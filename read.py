import json


def in_ra_man_hinh():
    # Mở file JSON
    with open("data.json", "r") as file:
        data = json.load(file)

    print(json.dumps(data, indent=4, select_keys=["name", "age"]))


if __name__ == "__main__":
    in_ra_man_hinh()
