'''
Created on 02/16/2020

@author: Junbo Lei
'''
RIGHT = 'R'
LEFT = 'L'
DOT = '.'
OCCUPIED = 'X' 


class Chamber:
    def animate(self, speed, init):
        print('speed: ' + speed)
        speed = int(speed)
        netInit = init.strip();
        print('init: ' + netInit)
        length = len(netInit)
        rightForward = []
        leftForward = []
        idx, rightLow, rightHigh, leftLow, leftHigh = -1, -1, -1, length, length
    
        for c in netInit:
            idx +=1
            if DOT == c:
                rightForward.append(DOT)
                leftForward.append(DOT)
            elif RIGHT == c:
                leftForward.append(DOT)
                rightForward.append(RIGHT)
                if rightLow < 0:
                    rightLow = idx
                    rightHigh = idx
                else:
                    rightHigh = idx
            else:
                rightForward.append(DOT)
                leftForward.append(LEFT)
                if leftLow == length:
                    leftLow = idx
                    leftHigh = idx
                else:
                    leftHigh = idx
                
        ret = []
        start = netInit.replace(RIGHT, OCCUPIED).replace(LEFT, OCCUPIED)
        ret.append(start)
        
        self.__startAnimate(speed, length, rightForward, leftForward, rightLow, rightHigh, leftLow, leftHigh, ret);
        
        totalRowNum = len(ret)
        lastRowNum = totalRowNum - 1 
        
        concatenated = '{'
        if totalRowNum == 1:
            concatenated = concatenated + '\"' + ret[lastRowNum] + '\"}' 
        else:
            for i in range(0, lastRowNum):
                concatenated = concatenated + '\"' + ret[i] + '\",\n'
            concatenated = concatenated + '\"' + ret[lastRowNum] + '\"}'
        
        return concatenated
    
    
    
    def __startAnimate(self, speed, length, rightForward, leftForward, rightLow, rightHigh, leftLow, leftHigh, ret):
        while (not self.__isChamberCleared(rightLow, rightHigh, leftLow, leftHigh, length)):
            if (not self.__isRightForwardCleared(rightLow, rightHigh, length)):
                self.__moveRight(speed, length, rightForward, rightLow, rightHigh)
                rightLow = rightLow + speed
                rightHigh = rightHigh + speed
            if (not self.__isLeftForwardCleared(leftLow, leftHigh, length)):
                self.__moveLeft(speed, leftForward, leftLow, leftHigh)
                leftLow = leftLow - speed
                leftHigh = leftHigh - speed
            chamberSnapShot = self.__getChamberSnapShot(length, rightForward, leftForward)
            ret.append(chamberSnapShot);
    
    def __getChamberSnapShot(self, length, rightForward, leftForward):
        s = ''
        for i in range(0, length):
            if rightForward[i] != leftForward[i]:
                s+=OCCUPIED
            else:
                s+=DOT
        return s
    
    def __moveLeft(self, speed, leftForward, leftLow, leftHigh):
        currentLeftHigh = leftHigh - speed
        if (currentLeftHigh < 0):
            self.__moveLeftOutBound(leftForward, leftHigh)
        else:
            self.__moveLeftInBound(speed, leftForward, leftLow, leftHigh)
    
    def __moveLeftInBound(self, speed, leftForward, leftLow, leftHigh):
        for i in range(leftLow, leftHigh + 1):
            if (i >= 0) and (leftForward[i] == LEFT):
                if ((i - speed) >= 0):
                    leftForward[i - speed] = leftForward[i]
                leftForward[i] = DOT
    
    def __moveLeftOutBound(self, leftForward, leftHigh):
        for i in range(leftHigh, -1, -1): 
            leftForward[i] = DOT
    
    def __moveRight(self, speed, length, rightForward, rightLow, rightHigh):
        currentRightLow = rightLow + speed;
        if (currentRightLow >= length):
            self.__moveRightOutBound(length, rightForward, rightLow)
        else:
            self.__moveRightInBound(speed, length, rightForward, rightLow, rightHigh)
    
    def __moveRightInBound(self, speed, length, rightForward, rightLow, rightHigh):
        for i in range(rightHigh, rightLow-1, -1):
            if (i < length) and (rightForward[i] ==RIGHT):
                if (i + speed) < length:
                    rightForward[i + speed] = rightForward[i]
                rightForward[i] = DOT
        
    
    def __moveRightOutBound(self, length, rightForward, rightLow):
        for i in range(rightLow, length):
            rightForward[i] = DOT
    
    def __isChamberCleared(self, rightLow, rightHigh, leftLow, leftHigh, totalLength):
        return self.__isRightForwardCleared(rightLow, rightHigh, totalLength) and self.__isLeftForwardCleared(leftLow, leftHigh, totalLength)
    
    def __isRightForwardCleared(self, rightLow, rightHigh, totalLength):
        return (rightLow < 0 and rightHigh < 0) or (rightLow >= totalLength)
    
    def __isLeftForwardCleared(self, leftLow, leftHigh, totalLength):                  
        return (leftLow == totalLength and leftHigh == totalLength) or (leftHigh < 0)
      


var = input('Please enter speed and init(separated by space):')
vrs = var.split()
chamber = Chamber() 
ret = chamber.animate(vrs[0], vrs[1])
print(ret)