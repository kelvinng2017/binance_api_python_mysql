# %%
column, row = 7, 13
start_list = [[" "]*row for _ in range(column)]

# %%
len(start_list[len(start_list)-1])
# %%
change_data = 6
change_left = 5
change_right = 7
for change_index in range(len(start_list)):
    print("change_index=%s" % change_index)
    if(change_index == 0):
        start_list[change_index][change_data] = "*"
        print(start_list)
    if(change_index >= 1):
        print("change_left=%s" % change_left)
        start_list[change_index][change_left] = "*"
        change_left = change_left - 1
        print("change_right=%s" % change_right)
        start_list[change_index][change_right] = "*"
        change_right = change_right + 1
        print(start_list)
    if(change_index == len(start_list)-1):
        print("最後一行")
        for change_row_index in range(len(start_list[change_index])):
            start_list[change_index][change_row_index] = "*"

# %%
start_list
# %%
for j in range(3):
    print(j)

# %%
