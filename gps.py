"""
Location
 1.isLocation 
   eval()을 통해 영역 포함 계산
Path
 1.

"""


from msilib.schema import Error
from threading import local
import numpy as np
from numpy.lib.function_base import gradient
from localmap import LocalMap
from map import Map
import math

class Location(): #금지 구역 설정

    def __init__(self) -> None:
        self.localmap = None
        self.borderCoord = []
        self.borderEquation = []
        self.IllegalArea = None

    def isLocation(self, coord, verbose=0):
        coord = self.localmap.location2D(coord)
        x = coord[1]
        y = coord[0]
        if self.borderEquation != []:
            equation = ''
            for idx, equation in enumerate(self.borderEquation):
                boundary = equation[0]
                gradient = equation[1]
                bias = equation[2]
                equation = str(y)+str(boundary)+str(gradient)+'*'+str(x)+str(bias) #Except '+' for it is negative value. #Return bool for whether isboundary
                equation2 = 'y'+str(boundary)+str(gradient)+'*'+'x'+str(bias) #Original Equation
                equation3 = str(gradient)+'*'+str(x)+str(bias) #Calulated value
                if verbose:
                    print(f'{idx}.')
                    print(eval(equation),' '*6,  equation2)
                    if verbose == 2:
                        print(f'Target: {y} Calcualted: {eval(equation3)}\n')
                if(not eval(equation)): return False
               # else: return True
        else:
            raise Error
        return True

    def isValid(self, coord):
        if self.isLocation(coord, verbose=0):
            return False
        return True


    def setIllegalArea(self, value):
        self.illegalArea = value

    def isIllegal(self):
        return False

class Path: #웨이포인트 설정
    def __init__(self, value=list() ,default=(37.5812,124.4310)) -> None:
        self.value = value
        self.start_point = default

    def set_GPS_controller(cls, GPS_Controller):
        cls.GPS_controller = GPS_Controller


    def add(self, value=None):
        if value == None:
            value = np.random.randn(2)
        self.value.append((value[0],value[1]))
        # if not self.location.isIllegal():
        #     self.value.append((value[0],value[1]))
        # else:
        #     raise ValueError('Not allowed point')
    
    def sampling_path(self, cnt, GPS_Controller, start_point=(37.5812,124.4310)):
        path = Path()
        f = open('sampling_path.txt','w')
        for i in range(cnt):
            if i == 0: loc = start_point
            else: loc = (loc[0]+np.random.uniform(-1,1), loc[1]+np.random.uniform(-1,1))
            if not GPS_Controller.location.isLocation([loc[0],loc[1]],2):
                path.add(loc)
                f.write(f'{loc[0]},{loc[1]}\n')
        f.close()

        return path

class GPSController:

    def __init__(self, file=None) -> None:
        self.gps_file = file
        self.location = Location()
        self.center = 37.9593, 124.6653

    def read(self, path='GPS.txt'):
        """
        read GPS file and chagne it into LocalMap
        path : GPS.txt
        """
        self.gps_file = path
        gps_coord = []

        f = open(path)
        for line in f.readlines():
            read_gps_coord = line.split(',')
            for i, coord in enumerate(read_gps_coord): #공백제거
                read_gps_coord[i] = round(float(coord.strip()), 4) 
            gps_coord.append(read_gps_coord)
        self.location.localmap = LocalMap(coords=gps_coord)
        self.location.borderCoord = gps_coord

        return True

    def calculate_equation(self, coord=None):
        """
        영역 포인트를 통해 직선의 방정식으로 영역 생성.
        """
        localmap = self.location.localmap
        assert localmap != None

        coord = self.location.borderCoord
        
        equation = []
        gradient='a'; bias='b'; boundary = '=='
        boundary_list = ['<','>','>','>','>','>','<','<']

        for idx, coord1 in enumerate(coord):
            if idx != len(coord)-1:
                coord2 = coord[idx+1]
            else:
                coord2 = coord[0]

            coord1 = localmap.location2D(coord1)
            coord2 = localmap.location2D(coord2)

            gradient = (coord2[0]-coord1[0])/(coord2[1]-coord1[1])
            bias1 = coord1[0]-coord1[1]*gradient
            bias2 = coord2[0]-coord2[1]*gradient
            bias = (bias1+bias2)/2
            boundary = boundary_list[idx]

            equation.append([boundary, gradient, bias])
        
        self.location.borderEquation.extend(equation)

        return True
    
    




def main():
    GPSControl = GPSController()
    GPSControl.read()
    GPSControl.calculate_equation()
    
    location = GPSControl.location

    co_BaekRyeongDo = (37.95156660478402, 124.6757830999149)
    #co_BaekRyeongDo = {"lat":37.9518,"lng":124.6757}
    # lat =  co_BaekRyeongDo['lat']
    # lng = co_BaekRyeongDo['lng']
    lat, lng = location.localmap.location2D([co_BaekRyeongDo[0],co_BaekRyeongDo[1]]) 

    print(f'현재 입력된 백령도 좌표: ({lat},{lng}): {location.isLocation((lat,lng))}')
    
    Path().set_GPS_controller(GPSControl)
    m = Map()
    while True:
        cnt = int(input('생성할 웨이포인트 수: '))
        path = Path().sampling_path(cnt, GPSControl)
        print(f'Waypoints have created: {path.value}')
        f = open('sampling_path.txt')
        lines = f.readlines()
        m.draw(lines)



main()
   