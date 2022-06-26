class targetType:
    disconnected = 0
    HDZero_Freestyle = 1
    HDZero_Race_v1 = 2
    HDZero_Race_v2 = 3
    HDZero_Whoop = 4
    HDZero_Whoop_Lite = 5
    unknow = 255

def targetDetect():
    print('targetType:',targetType.HDZero_Freestyle)
    return targetType.HDZero_Freestyle