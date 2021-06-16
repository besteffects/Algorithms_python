# A list of elements is given. The most of elements of this list have pairs, e.g. two elements. But some elements do
# not have pairs. Find elements without pairs

elements = [2, 1, 5, 2, 4, 3, 1, 4]
solution_dict = {}
for item in elements:
    if item in solution_dict:
        solution_dict[item] = solution_dict.get(item, 0) + 1
    if not solution_dict.get(item, None):
        solution_dict[item] = 1
for key, value in solution_dict.items():
    if value == 1:
        print(key)
