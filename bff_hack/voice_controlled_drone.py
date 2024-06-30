from vosk import Model, KaldiRecognizer
import pyaudio
from djitellopy import Tello
import cv2
from utils import Action, get_tello_video
from threading import Thread


drone = Tello()
drone.connect()
print(f"BATTERY : {drone.get_battery()}%")


classFile = 'gesture.names'
with open(classFile, 'rt') as f:
    classNames = f.read().split('\n')
    print()
    print()
    print()
    print(classNames)
    print()
    print()

model= Model(r"/Users/ratanprakash/Desktop/bff_hack/vosk-model-small-en-in-0.4")
recognizer = KaldiRecognizer(model, 16000)


mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

def main():
    while True:
        data = stream.read(4896)

        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            print(text[14:-3])
            command = text[14:-3]
            if command == "exit":
                break
            # Action(command, drone)
            window = tk.Tk()
            window.geometry("400x200") # set the size of the window
            label = tk.Label(window, text="", font=("Arial", 30)) # set the font size of the label widget
            label.pack()

            update_text()

window.mainloop()


droneCam = Thread(target = get_tello_video(drone))
main = Thread(target=main)
droneCam.start()
main.start()
droneCam.join()
main.join()

drone.streamoff()
cv2.destroyAllWindows()


