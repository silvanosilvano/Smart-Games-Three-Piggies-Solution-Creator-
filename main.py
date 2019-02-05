"""
title： 三只小猪Three Piggies
original game copyright: Smart Games
author：silvano.cheng@gmail.com
Date and time: 2019年2月4日,5日


"""

CURRENT_BOARD = [(2,1),(3,1),
                 (1,2),(2,2),(3,2),(4,2),
                 (1,3),(2,3),(3,3),(4,3),
                 (2,4),(3,4),(4,4)]

# print(CURRENT_BOARD[19])
# 测试board的情况

PG1 = (2,3)
PG2 = (4,2)
PG3 = (1,2)

Wlf = (1, 3)


PIGS = [PG1, PG2]

ALL_COLORS = ["r", "y", "b"]


def occu_house(color, pos, rotation):
    a = pos[0]
    b = pos[1]
    if color == "r":
        return occu_house_r(a, b, rotation)
    elif color == "y":
        return occu_house_y(a, b, rotation)
    elif color == "b":
        return occu_house_b(a, b, rotation)


def occu_house_y(a,b,rotation):
    if rotation == 0:
        # 正方形左上角直角
        return (a,b),(a,b+1),(a+1,b)  # 此数据为手写。改进时可以输入（a,b）时套用规则
    elif rotation == 1:
        # 顺时针转90度
        return (a,b),(a-1,b),(a,b+1)  # 纯手写，numpy应该有类似matrix旋转的处理法
    elif rotation == 2:
        return (a,b),(a,b-1),(a-1,b)
    elif rotation == 3:
        return (a,b),(a+1,b),(a,b-1)


def occu_house_r (a,b, rotation):
    if rotation == 0:
        # 正方形左上角直角
        return (a,b),(a,b+1),(a+1,b), (a+2,b)  # 此数据为手写。改进时可以输入（a,b）时套用规则
    elif rotation == 1:
        # 顺时针转90度
        return (a,b),(a-1,b),(a,b+1),(a,b+2)  # 纯手写，numpy应该有类似matrix旋转的处理法
    elif rotation == 2:
        return (a,b),(a,b-1),(a-1,b),(a-2,b)
    elif rotation == 3:
        return (a,b),(a+1,b),(a,b-1),(a,b-2)


def occu_house_b(a,b,rotation):
    if rotation == 0 or rotation == 2:
        # 横着一排
        return (a,b),(a-1,b),(a+1,b)
    elif rotation == 1 or rotation == 3:
        return (a,b),(a,b+1),(a, b-1)


def check_in_board(house_occu, board):
    """
    :param house_occu: 输入house的所有位置
    :param board: 现有的board情况
    :return: True还是False

    """
    for dot in house_occu:
        if dot in board:
            continue
        else:
            return False
    return True


def check_house_collide(house1, house2):
    # print("entering check_house_collide")
    for pos in house2:
        if pos in house1:
            # print("collision!", "house2 pos",pos, "house1", house1)
            return True
    return False


def calculate_house(board, color_type):
    """
    :param board: 现在剩下的board
    :param occu_house_color: 哪一种函数
    :return: temp_board，（house种类，初始位置，rotation）
    """
    if color_type == "r":
        occu_house_color = occu_house_r
    elif color_type == "b":
        occu_house_color = occu_house_b
    elif color_type == "y":
        occu_house_color = occu_house_y

    temp_board = []

    for pos in board:
        for rot_num in [0, 1, 2, 3]:
            single_occu = occu_house_color(*pos, rot_num)
            if check_in_board(single_occu, board):
                temp_board.append((color_type, pos, rot_num))

    return temp_board


# start:
occupied_board = CURRENT_BOARD[:]


# 现有游戏中每个house单独摆放的所有的可能性

all_result = []
for c in ALL_COLORS:
    all_result.append(calculate_house(occupied_board, c))

# print(len(all_result))
# print(len(all_result[0]) + len(all_result[1]) + len(all_result[2]) )
# print(all_result)


# 所有的组合可能性

possible_combi = []    #list of list

for first_house in all_result[0]:
    # first house，包括（color，(position, position), rotation).
    # 实际颜色:r, 匹配ALL_COLORS顺序

    first_house_occupation = occu_house_r(*first_house[1],first_house[2])
    # print("f house, occu", first_house_occupation)

    for second_house in all_result[1]:
        #实际颜色y
        # print(second_house[1],first_house[1],second_house[1]==first_house[1])
        second_house_occupation = occu_house_y(*second_house[1],second_house[2])  # 这里是直接输入的。可以加入检查second_house[0]的属性是r,b还是y
        #todo 已加occu_house函数，等待更改
        # print("second house_occupation", second_house_occupation)

        if check_house_collide(first_house_occupation, second_house_occupation):
            # print("collide:True")
            continue
        else:
            # print("secind stage: collide: False. Entering third stage")
            for third_house in all_result[2]:
                # 实际颜色brown
                third_house_occupation = occu_house_b(*third_house[1], third_house[2])
                if check_house_collide(first_house_occupation,third_house_occupation) or \
                        check_house_collide(second_house_occupation, third_house_occupation):
                    continue
                else:
                    # print("result", "house1,2,3", first_house,second_house,third_house)
                    possible_combi.append((first_house,second_house,third_house))

# print(len(possible_combi))
# print(possible_combi)
# print(possible_combi[15])


def pig_collide(pg_pos, one_combi):
    for one_colored_house in one_combi:
        if pg_pos in occu_house(*one_colored_house):
            # print("collision! pg_pos", pg_pos, "house", one_colored_house)
            return True
    # print("pg ok! ")
    return False


def pig_inside(pg, one_combi):
    for one_colored_house in one_combi:
        if pg in one_colored_house:
            return True
    return False


def all_pgs_inside_house(pgs, one_combi):
    for pg in pgs:
        # print("pg, one_combi:",pg,one_combi)
        if pig_inside(pg, one_combi):
            # print("pg inside")
            continue
        else:
            return False
    # print("all_pgs_inside_houes!pgs:", pgs,"one_combi",one_combi )
    return True


def all_pgs_outside_house(pgs,one_combi):
    for one_pg in pgs:
        if pig_collide(one_pg, one_combi):
            return False
    return True


def wolf_outside_house(wlf, one_combi):
    if pig_collide(wlf, one_combi):
        return False
    else:
        return True


def day_pigs(pgs, possible_combi):
    winners = []
    for one_combi in possible_combi:
        if all_pgs_outside_house(pgs,one_combi):
            # print("We have the winner!/n The combination is:",one_combi, "/n And the pigs are in pos:", pgs)
            winners.append(one_combi)
    # print(len(winners),"winners \n", winners)
    return winners


def night_pigs(pgs, wlf, possible_combi):
    winners = []
    for one_combi in possible_combi:
        if all_pgs_inside_house(pgs, one_combi) and wolf_outside_house(wlf, one_combi):
            winners.append(one_combi)
            # print("We have the winner!\n The combination is:", one_combi, "\n And the pigs are in pos:", pgs,
            # "and the wolf", wlf)
    # print(len(winners), "winners \n", winners)
    return winners


def game_start(possible_combi):
    n_of_pgs = int(input("How many pigs?\n"))
    pgs = []
    winner = []
    for i in range(n_of_pgs):
        pg_pos = input("Input pig n.%s in a, b form, like 2,1\n"%(i+1) )
        pg_pos_int = (int(pg_pos[0]), int(pg_pos[2]))
        pgs.append(pg_pos_int)

    print("\n Ok. There are %s pigs.They are %s \n"%(n_of_pgs,pgs))

    n_of_wlfs = int(input("How many wolfs? Enter 0 or 1. \n"))
    if n_of_wlfs == 0:
        wlf = 0
        winner = day_pigs(pgs, possible_combi)
    elif n_of_wlfs == 1:
        wlf_pos = input("Please enter wolf position, as in a,b form.\n")
        wlf = (int(wlf_pos[0]), int(wlf_pos[2]))
        print("\nOk. Wolf pos:\n", wlf)
        winner = night_pigs(pgs, wlf, possible_combi)
    # print(winner)
    draw_board(pgs, wlf, winner)


def draw_board(pgs, wlf, solution):
    # 建立空board
    one_line_board = ["X"]* 4
    final_board = []
    for i in range(4):
        final_board.append(one_line_board[:])

    #将空board上的部位替换掉
    empty_angles = [(0,0),(0,3),(3,0)]
    for angle in empty_angles:
        final_board[angle[0]][angle[1]] = "."

    #将猪和狼放在board上
    for pg in pgs:
        final_board[pg[1]-1][pg[0]-1] = "P"

    if wlf != 0:
        final_board[wlf[1]-1][wlf[0]-1] = "W"

    # 打印出来
    for ln in final_board:
        for item in ln:
            print(item,end='     ')
        print("\n")

    # 游戏结果
    print("\n" *3)
    print("答案如下：")
    print("\n")

    if len(solution) == 0:
        print ("无解")
        return
    #else:
        #print(solution)

    for one_house in solution[0]:
        house_occu = occu_house(*one_house)
        for one_pos in house_occu:
            house_symbol = ''
            final_board[one_pos[1]-1][one_pos[0]-1] = "%s"%one_house[0].capitalize()

    # 打印结果
    for ln in final_board:
        for item in ln:
            print(item, end='     ')
        print("\n")



game_start(possible_combi)
