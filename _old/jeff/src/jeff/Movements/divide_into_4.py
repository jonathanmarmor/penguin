from random import shuffle

def divide_into_4(n):
    """return four integers that somewhat evenly subdivide n"""
    div = n / 4
    if n % 4 == 0:
        return [div]*4
    if n % 4 == 1:
        result = [div]*3
        result += [div+1]
        shuffle(result)
    if n % 4 == 2:
        result = [div]*2
        result += [div+1]*2
        shuffle(result)        

    if n % 4 == 3:
        result = [div]
        result += [div+1]*3
        shuffle(result)
    return result

if __name__ == '__main__':
    print divide_into_4(21)