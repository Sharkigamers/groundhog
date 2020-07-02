#!/usr/bin/env python3

##
## EPITECH PROJECT, 2020
## groundhog
## File description:
## groundhog
##

import sys
import operator
import signal
from math import sqrt

class Groundhog():
    def __init__(self, period):
        self.period = self.checkInteger(period)
        if (self.period <= 0):
            help()
            exit(0)
        self.loopCounter = 0
        self.lastG = None
        self.lastR = None
        self.lastS = None
        self.g = None
        self.r = None
        self.s = None
        self.switch = None
        self.switchTime = 0
        self.tempData = []
        self.weirdestValues = {}
        self.printWeirdestValues = []

    def mainLoop(self):
        line = input("")
        while (line != "STOP"):
            self.score = 0
            self.tempData.append(float(line))
            self.loopCounter = len(self.tempData)
            self.setSwitch(line)
            self.lastG = self.g
            self.lastR = self.r
            self.lastS = self.s
            self.calculateTemperatureIncreaseAverage()
            self.calculateRelativeTemperatureEvolution()
            self.calculateStandardDeviation()
            self.displayResult()
            line = input("")
        if (self.loopCounter <= self.period):
            exit(84)
        self.findWeirdestValues()
        print("Global tendency switched {} times".format(self.switchTime))
        print("{} weirdest values are {}".format(len(self.printWeirdestValues), self.printWeirdestValues))

    def setSwitch(self, line):
        if (self.switch == None):
            if (float(line) > 0):
                self.switch = True
            elif (float(line) < 0):
                self.switch = False

    def calculateStandardDeviation(self):
        if (self.loopCounter >= self.period):
            mu = 0
            sigma = 0
            for i in range(self.loopCounter - self.period, self.loopCounter):
                mu += self.tempData[i]
            mu /= self.period
            for i in range(self.loopCounter - self.period, self.loopCounter):
                sigma += pow((self.tempData[i] - mu), 2)
            try:
                self.s = sqrt(sigma / self.period)
            except:
                self.s = float('nan')

    def calculateRelativeTemperatureEvolution(self):
        if (self.loopCounter > self.period):
            try:
                self.r = int(round((self.tempData[-1] - self.tempData[-1 - self.period]) / sqrt(pow(self.tempData[-1 - self.period], 2)) * 100))
            except:
                self.r = float('nan')

    def calculateTemperatureIncreaseAverage(self):
        if (self.loopCounter > self.period):
            self.g = 0
            for i in range(self.loopCounter - self.period, self.loopCounter):
                tempIncrease = self.tempData[i] - self.tempData[i - 1]
                if (tempIncrease > 0):
                    self.g += tempIncrease
                else:
                    self.g += 0
            try:
                self.g = self.g / self.period
            except:
                self.g = float('nan')


    def displayResult(self):
        print("g=", end='')
        if (self.loopCounter <= self.period):
            print("nan", end='\t')
        else:
            print("{:.2f}".format(self.g), end='\t')
        print("r=", end='')
        if (self.loopCounter <= self.period):
            print("nan%", end='\t')
        else:
            print("{}%".format(self.r), end='\t')
        print("s=", end='')
        if (self.loopCounter < self.period):
            print("nan", end='')
        else:
            print("{:.2f}".format(self.s), end='\t')
        if (self.switch != None and self.r != None):
            if (self.switch == False and self.r >= 0):
                print("\ta switch occurs", end='')
                self.switch = True
                self.switchTime += 1
            elif (self.switch == True and self.r < 0):
                print("\ta switch occurs", end='')
                self.switch = False
                self.switchTime += 1
        print("")

    def findWeirdestValues(self):
        lengthTempData = len(self.tempData)

        for i in range (0, lengthTempData):
            if (i + 3 > lengthTempData):
                break
            try:
                thirdValue = (self.tempData[i] + self.tempData[i + 2]) / 2
                weirdValue = sqrt(pow(thirdValue - self.tempData[i + 1], 2))
            except:
                weirdValue = 0

            if (self.tempData[i + 1] not in self.weirdestValues or
            (self.tempData[i + 1] in self.weirdestValues and
            self.weirdestValues[self.tempData[i + 1]] < weirdValue)):
                self.weirdestValues[self.tempData[i + 1]] = weirdValue
        self.weirdestValues = dict(sorted(self.weirdestValues.items(), key=operator.itemgetter(1),reverse=True))
        i = 0
        for key in self.weirdestValues:
            if (i >= 5):
                break
            self.printWeirdestValues.append(key)
            i += 1

    def checkInteger(self, arg):
        try:
            if (len(str(int(arg))) != len(arg)):
                exit(84)
        except:
            exit(84)
        return int(arg)

def help():
    try:
        with open("HELP.txt", "r") as file:
            print(file.read())
    except:
        exit(84)

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        exit(84)
    if (sys.argv[1] == "-h"):
        help()
    elif (sys.argv[1]):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)
        try:
            groundhog = Groundhog(sys.argv[1])
            groundhog.mainLoop()
        except:
            exit(84)
    exit(0)
