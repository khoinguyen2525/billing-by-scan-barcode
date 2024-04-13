import cv2
from pyzbar.pyzbar import decode
import json
import time

data_list = {"data": []}


def read_code(image_path):
    # Read the image
    image = cv2.imread(image_path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Decode QR codes
    qr_codes = decode(gray)
    # Process QR code data
    for qr_code in qr_codes:
        data = qr_code.data.decode("utf-8")
        ten = str(input("nhap ten: "))
        gia = str(input("nhap gia sp: "))
        datas = [data, ten, gia]
        data_list.append(datas)
    return data_list

def scan_code():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # 3 = width
    cap.set(4, 480)  # 4 = height
    camera = True

    data_list = json.load(open("data.json"))
    used_codes = []

    while True:
        items = data_list["data"]
        for item in items:
            code = item["code"]
            used_codes.append(code)

        while camera == True:
            success, frame = cap.read()

            for code in decode(frame):
                if code.data.decode("utf-8") not in used_codes:
                    print("processing.....")
                    print(code.type)
                    print(code.data.decode("utf-8"))
                    name = input("Enter name: ")
                    price = input("Enter price (in VND): ")
                    data_list["data"].append(
                        {
                            "name": name,
                            "price": price,
                            "code": code.data.decode("utf-8"),
                        }
                    )
                    time.sleep(2)
                    print("loading......")
                    # Save the data
                    with open("data.json", "w") as file:
                        json.dump(data_list, file, indent=4)
                    try:
                        with open("data.json", "r") as file:
                            data_list = json.load(file)
                    except FileNotFoundError:
                        data_list = {"data": []}

                    # Add new objects as before
                    # ...

                    # Save the updated data
                    with open("data.json", "w") as file:
                        json.dump(data_list, file, indent=4)
                    items = data_list["data"]
                    for item in items:
                        code = item["code"]
                        used_codes.append(code)
                elif code.data.decode("utf-8") in used_codes:
                    print("this code is recognised")
                    time.sleep(2)
                    print("loading........")
                    return data_list
                else:
                    pass
            cv2.imshow("scan", frame)
            cv2.waitKey(1)


def save_data_list():
    while True:
        name = input("Enter name (or 'q' to quit): ")
        if name == "q":
            break
        price = input("Enter price (in VND): ")
        code = input("........: ")
        data_list["data"].append({"name": name, "qr_code": price, "code": code})

    # Save the data
    with open("data.json", "w") as file:
        json.dump(data_list, file, indent=4)
    try:
        with open("data.json", "r") as file:
            data_list = json.load(file)
    except FileNotFoundError:
        data_list = {"data": []}

    # Add new objects as before
    # ...

    # Save the updated data
    with open("data.json", "w") as file:
        json.dump(data_list, file, indent=4)


if __name__ == "__main__":
   scan_code()
