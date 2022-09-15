import json

# import fileinput

# file_name = "ingredients_converted.json"

# for line in fileinput.FileInput(file_name, inplace=1):
#     # print(line.find('{'))
#     print line ,

# with open("ingredients_converted.json", "r") as f:
#     contents = f.readlines()

# contents.insert(index, value)

# with open("path_to_file", "w") as f:
#     contents = "".join(contents)
#     f.write(contents)


# f = open('ingredients_converted.json', 'w+')
# print(f)
# f.close()
f1 = open("ingredients.json", "r")
json_object = json.load(f1)
i = 1
f2 = open("ingredients_converted1.json", "w")
json_object_converted = []
for element in json_object:
    element.update({"id": i})
    i += 1
    # json.dump(element, f2)    
    json_object_converted.append(element)
json_object_converted = str(json_object_converted)
# print(json_object_converted)
f2.write(json_object_converted)
# print(json_object_converted)
# json_object_converted_serialized = json.dumps(list)

# json.dump(json_object_converted, f2)
# f2.write(json_object_converted_serialized)
# print(f1.readlines())

f1.close()
f2.close()