level = int(input("请输入行数："))
# 方式一：
for current_level in range(1, level+1):
    #print("current_leve=%s" % current_level)
    # 控制空格个数
    for i in range(level-current_level):
        #print("i=%s" % i)
        print(' ', end='')
    # 控制*个数
    for j in range(2*current_level-1):
        # print(2*current_level-1)
        if(current_level != level):
            if(j == 0 or j == (2*current_level-1)-1):
                print('*', end='')
            else:
                print(' ', end='')
        else:
            print('*', end='')
    print()
