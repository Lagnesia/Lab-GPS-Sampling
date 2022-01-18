import numpy as np

class Location(): #금지 구역 설정

    def __init__(self) -> None:
        self.IllegalArea = None

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


def main():
    co_BaekRyeongDo = {"lat":37.5812,"lng":124.43}
    lat = co_BaekRyeongDo['lat']
    lng = co_BaekRyeongDo['lng']
    print(f'현재 입력된 백령도 좌표: ({lat},{lng})')
    while True:
        cnt = int(input('생성할 웨이포인트 수: '))
        path = Path.create_path(Path, cnt)
        print(f'Waypoints have created: {path.value}')



main()
   