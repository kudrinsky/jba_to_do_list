user_input = input().lower().split()
dict_in = {}
for item in user_input:
    if item not in dict_in:
        dict_in[item] = user_input.count(item)

for key, value in dict_in.items():
    print(key, value)