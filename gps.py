from msilib.schema import Error
import numpy as np
from numpy.lib.function_base import gradient

class Location(): #금지 구역 설정

    def __init__(self) -> None:
        self.location = []
        self.location_coord = []
        self.IllegalArea = None

    def isLocation(self, coord):
        x = coord[1]
        y = coord[0]
        if self.location != []:
            equation = ''
            for equation in self.location:
                boundary = equation[0]
                gradient = equation[1]
                bias = equation[2]
                equation = str(y)+str(boundary)+str(gradient)+'*'+str(x)+'+'+str(bias)
                equation2 = 'y'+str(boundary)+str(gradient)+'*'+'x'+'+'+str(bias)
                print(eval(equation), equation2)
                if(not eval(equation)): pass
               # else: return True
        else:
            raise Error
        return False

    def setIllegalArea(self, value):
        self.illegalArea = value

    def isIllegal(self):
        return False

class Path: #웨이포인트 설정
    
    def __init__(self, value=list(), default=(37.5812,124.43)) -> None:
        self.value = value
        self.location = Location()
        self.start_point = default


    def add(self, value=None):
        if value == None:
            value = np.random.randn(2)
        if not self.location.isIllegal():
            self.value.append((value[0],value[1]))
        else:
            raise ValueError('Not allowed point')
    
    def create_path(cls, cnt, start_point=(37.5812,124.43)):
        path = Path()
        for i in range(cnt):
            if i == 0: loc = start_point
            else: loc = (start_point[0]+np.random.randn(1)[0], start_point[1]+np.random.randn(1)[0])
            path.add(loc)
        return path

class GPSController:

    def __init__(self, file=None) -> None:
        self.gps_file = file
        self.location = Location()

    def read(self, path='GPS.txt'):
        """
        path를 읽고 영역 포인트를 저장
        (n,2) 크기 list[]
        """
        self.gps_file = path

        f = open(path)
        for line in f.readlines():
            gps_coord = line.split(',')
            for i, coord in enumerate(gps_coord): #공백제거
                gps_coord[i] = float(coord.strip())
            self.location.location_coord.append(gps_coord)

        return True

    def calculate_equation(self, coord=None):
        """
        영역 포인트를 통해 직선의 방정식으로 영역 생성.
        """
        coord = self.location.location_coord
        
        equation = []
        gradient='a'; bias='b'; boundary = '=='
        boundary_list = ['<','>','>','>','>','>','<','<']

        for idx, coord1 in enumerate(coord):
            if idx != len(coord)-1:
                coord2 = coord[idx+1]
            else:
                coord2 = coord[0]

            gradient = (coord2[0]-coord1[0])/(coord2[1]-coord1[1])
            bias1 = coord1[0]-coord1[1]*gradient
            bias2 = coord2[0]-coord2[1]*gradient
            bias = (bias1+bias2)/2
            boundary = boundary_list[idx]

            equation.append([boundary, gradient, bias])
        
        self.location.location.extend(equation)

        return True
    
    




def main():
    GPSControl = GPSController()
    GPSControl.read()
    GPSControl.calculate_equation()
    
    location = GPSControl.location

    co_BaekRyeongDo = {"lat":37.5812,"lng":124.43}
    lat = co_BaekRyeongDo['lat']
    lng = co_BaekRyeongDo['lng']

    print(f'현재 입력된 백령도 좌표: ({lat},{lng}): {location.isLocation((lat,lng))}')
    while True:
        cnt = int(input('생성할 웨이포인트 수: '))
        path = Path.create_path(Path, cnt)
        print(f'Waypoints have created: {path.value}')



main()
   