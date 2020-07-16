# The following line creates a dictionary from the input. Do not modify it, please
test_dict = json.loads(input())

print('min:', min(test_dict, key=test_dict.get))
print('max:', max(test_dict, key=test_dict.get))
