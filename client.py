import socket
import pyaudio
from threading import Thread
from colorama import *


def main():
    # PYAUDIO SETTINGS
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    MONO = 1
    RATE = 20000

    # SOCKET SETTINGS

    HOST = "192.168.1.77"
    PORT = 32789
    SERVER_BIND = (HOST, PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((HOST, PORT))
    print(Fore.GREEN + "[+] Connected to: " + HOST + Style.RESET_ALL)
    print(Fore.GREEN + "[+] Listening..." + Style.RESET_ALL)
    ### MAIN CODE ###

    AUDIO = pyaudio.PyAudio()
    recieve_stream = AUDIO.open(format=FORMAT, channels=MONO, rate=RATE, output=True, frames_per_buffer=CHUNK)
    send_stream = AUDIO.open(format=FORMAT, channels=MONO, rate=RATE, input=True, frames_per_buffer=CHUNK)


    def recieve_voicestream():
        while True:
            try:
                data, server = s.recvfrom(CHUNK)
                recieve_stream.write(data)
            except:
                pass

    def send_voicestream():
        while True:
            try:
                datasend = send_stream.read(CHUNK)
                s.sendto(datasend, SERVER_BIND)
            except:
                pass

    RECIEVE_THREAD = Thread(target=recieve_voicestream)
    TRANSMIT_THREAD = Thread(target=send_voicestream)

    RECIEVE_THREAD.start()
    TRANSMIT_THREAD.start()

    while True:
        pass

if __name__ == '__main__':
    main()