#!/usr/bin/env python
# coding:utf-8

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

mousePositionX = 0
mousePositionY = 0

X = []
Y = []

data = []
DataFileName = "usbdat.txt"

def main():
    global mousePositionX
    global mousePositionY
    # check argv
    if len(sys.argv) != 3:
        print("步骤1 : 请先手动提取出鼠标的轨迹数据。")
        print("步骤2 : tshark -r mouse.pcap -T fields -e usb.capdata > usbdata.txt")
        print("        python UsbMiceHacker.py data.pcap [LEFT|RIGHT|MOVE|ALL]")
        print("Tips : ")
        print("        To use this python script , you must install the numpy,matplotlib first.")
        print("        You can use `sudo pip install matplotlib numpy` to install it")
        print("Author : ")
        print("        WangYihang <wangyihanger@gmail.com>")
        exit(1)

    # get argv
    pcapFilePath = sys.argv[1]
    action = sys.argv[2]

    if action != "LEFT" and action != "ALL" and action != "RIGHT" and action != "MOVE":
        action = "LEFT"

    # get data of pcap
    """
    command = "tshark -r %s -T fields -e usb.capdata > %s" % (
        pcapFilePath, DataFileName)
    print(command)
    os.system(command)
    """
    # read data
    with open(DataFileName, "r") as f:
        for line in f:
            data.append(line[0:-1])

    # handle move
    for i in data:
        """
        Bytes = i.split(":")
        if len(Bytes) == 8:
            horizontal = 2  # -
            vertical = 4  # |
        elif len(Bytes) == 4:
            horizontal = 1  # -
            vertical = 2  # |
        else:
            continue
            """
        Bytes = i
        if len(Bytes) == 16:
            horizontal = 4
            vertical = 8
            offsetX = int(Bytes[4:6],16)
            offsetY = int(Bytes[8:10],16)
        elif len(Bytes)==8:
            horizontal = 2
            vertical = 4
            offsetX = int(Bytes[2:4],16)
            offsetY = int(Bytes[4:6],16)
        else:
            continue
        #print(Bytes, Bytes[horizontal], int(Bytes[horizontal], 16), Bytes[vertical], int(Bytes[vertical], 16))
        #offsetX = int(Bytes[horizontal:horizontal+2], 16)
        #offsetY = int(Bytes[vertical], 16)
        print(i, offsetX, offsetY)
        if offsetX > 127:
            offsetX -= 256
        if offsetY > 127:
            offsetY -= 256
        mousePositionX += offsetX
        mousePositionY += offsetY
        if Bytes[0:2] == "01":
            print("[+] Left butten.")
            if action == "LEFT":
                # draw point to the image panel
                X.append(mousePositionX)
                Y.append(-mousePositionY)
        elif Bytes[0:2] == "02":
            print("[+] Right Butten.")
            if action == "RIGHT":
                # draw point to the image panel
                X.append(mousePositionX)
                Y.append(-mousePositionY)
        elif Bytes[0:2] == "00":
            print("[+] Move.")
            if action == "MOVE":
                # draw point to the image panel
                X.append(mousePositionX)
                Y.append(-mousePositionY)
        else:
            print("[-] Known operate.")
            pass
        if action == "ALL":
            # draw point to the image panel
            X.append(mousePositionX)
            Y.append(-mousePositionY)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.set_title('[%s]-[%s] Author : WangYihang' % (pcapFilePath, action))
    ax1.scatter(X, Y, c='r', marker='o')
    plt.show()

    # clean temp data
    os.system("rm ./%s" % (DataFileName))

if __name__ == "__main__":
    main()
