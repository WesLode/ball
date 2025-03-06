
from  bisect import bisect_left

def lookup_array(x, arrayy):
    cc =0
    for i in arrayy:
        if x <= i:
            return cc
        else:
            cc = cc + 1
def holeSize(array):
    hole = []
    for i in range(len(array)-1):
        # print(f'i: {i}')
        hole = hole + [ array[i+1] -array[i]]
    # print(f'Hole: {hole}')
    return hole

def getResults(queries):
    max_hole_location = []
    bar_col = [0]

    result = []

    for i in queries:
        if i[0] == 1:
            bar_col.append(i[1])
        # elif i[0] == 2:
        max_hole_location.append(i[1])
    bar_col.sort()
    bar_col = bar_col + [max(max_hole_location)]
    print(bar_col)

    for k in reversed(queries):
        # print(bar_col)
        if k[0] == 1:
            # print(f'theis {k[1]}')
            bar_col.remove(k[1])

        elif k[0] == 2:
            print(f'value: {k}')
            x=lookup_array(k[1], bar_col)
            print(f'bar_col: {bar_col}')
            print(f'lookup_array: {x}')
            print(f'bar_col[:x]:{bar_col[:x] + [k[1]]}')
            y = holeSize(bar_col[:x] + [k[1]])
            print(max(y + [-1]))
            result.append( k[2] <= max(y))
    print(f'result = {result}')

    result.reverse()
    return result



# queries =[[1,2],[2,3,3],[2,3,1],[2,2,2]]
# queries =[[1,7],[2,7,6],[1,2],[2,7,5],[2,7,6]]
queries = [[1,4],[2,1,2]]
a=getResults(queries)
# testArray = [0, 2,3]
# z = holeSize(testArray)
# print(max(z))
# print(a)