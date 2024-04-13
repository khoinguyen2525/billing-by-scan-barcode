import cv2
from pyzbar.pyzbar import decode
import json
from difflib import get_close_matches
import time
import pyttsx3
import speech_recognition as sr
import datetime

friday = pyttsx3.init()
voice = friday.getProperty("voices")
friday.setProperty("voice", voice[1].id)


def speak(audio):
    print("EDEN: " + audio)
    friday.say(audio)
    friday.runAndWait()


def welcome():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("good moring sir")
    elif hour >= 12 and hour < 18:
        speak("good afternoon sir")
    else:
        speak("good night sir")
    speak("how can i help you ?")


def billing():
    scanned_items = []
    total_price = 0
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # 3 = width
    cap.set(4, 480)  # 4 = height
    camera = True
    with open("data.json", "r") as json_file:
        data_list = json.load(json_file)
    print("scanning")
    while camera == True:
        success, frame = cap.read()
        codes = decode(frame)

        for code in codes:
            # Extract the decoded data
            print(code.type)
            print(code.data.decode("utf-8"))
            user_input = code.data.decode("utf-8")

            # Search for the code in the JSON data
            found_item = next(
                (item for item in data_list["data"] if item["code"] == user_input), None
            )

            # Check if the code was found
            if found_item:
                name = found_item["name"]
                price = int(found_item["price"])
                total_price += price
                print(f"Name: {name}, Price: {price}")
                scanned_items.append({"name": name, "price": price})
                time.sleep(2)

            else:
                print("Code not found in JSON file")

        # Display the frame
        cv2.imshow("Barcode Scanner", frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()
    print(".........................................................................")
    print("List scanned items:")
    for item in scanned_items:
        print(f"Name: {item['name']}, Price: {item['price']} " + " VND")

    print(f"Total Price: {total_price}" + " VND")


if __name__ == "__main__":

    billing()
