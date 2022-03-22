

arr = ["NORTH", "SOUTH", "SOUTH", "EAST", "WEST", "NORTH", "WEST"]

def dirReduc(arr):
    steps = []  #
    for step in arr:  #
        steps.append(step)
        if "EAST" in steps[-2:] and "WEST" in steps[-2:]:
            steps.pop(-1)
            steps.pop(-1)
        elif "NORTH" in steps[-2:] and "SOUTH" in steps[-2:]:
            steps.pop(-1)
            steps.pop(-1)

    for step in steps:  #
        if "EAST" in steps[-2:] and "WEST" in steps[-2:]:
            steps.pop(-1)
            steps.pop(-1)
        elif "NORTH" in steps[-2:] and "SOUTH" in steps[-2:]:
            steps.pop(-1)
            steps.pop(-1)
    return steps


def dirReduc2(arr):
    opposite = {'NORTH': 'SOUTH', 'EAST': 'WEST', 'SOUTH': 'NORTH', 'WEST': 'EAST'}
    new_plan = []
    [new_plan.pop() if new_plan and new_plan[-1] == opposite[d] else new_plan.append(d) for d in arr]
    return new_plan


def dirReduc3(arr):
    dir = " ".join(arr)
    dir2 = dir.replace("NORTH SOUTH",'').replace("SOUTH NORTH",'').replace("EAST WEST",'').replace("WEST EAST",'')
    dir3 = dir2.split()
    return dirReduc(dir3) if len(dir3) < len(arr) else dir3


def dirReduc4(arr):
    opposites = [{'NORTH', 'SOUTH'}, {'EAST', 'WEST'}]
    for i in range(len(arr) - 1):
        if set(arr[i:i + 2]) in opposites:
            del arr[i:i + 2]
            return dirReduc(arr)
    return arr


def dirReduc5(arr):
    opposite={"NORTH":"SOUTH",
              "SOUTH":"NORTH",
              "WEST":"EAST",
              "EAST":"WEST"
    }
    i=0
    while i+1<len(arr):
        opp=opposite.get(arr[i])
        if arr[i+1]==opp:
            arr.pop(i+1)
            arr.pop(i)
            i=0
        else:
            i+=1
    return arr


def dirReduc6(arr):
    opposite = {"NORTH": "SOUTH",
                "SOUTH": "NORTH",
                "WEST": "EAST",
                "EAST": "WEST"
                }
    i = 0
    while i+1 < len(arr):
        opp = opposite.get(arr[i])
        if arr[i+1] == opp:
            arr.pop(i+1)
            arr.pop(i)
            if i > 0:
                i -= 1
        else:
            i += 1
    return arr
  
