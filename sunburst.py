import json

## load file and parse it
sunburst_response_file = open("resources/sunburst_response.json","r")
sunburst_response = sunburst_response_file.readlines()[0]
parsed_response = json.loads(sunburst_response)

# root elements
max_depth = parsed_response["maxDepth"] #steps
elements = parsed_response["elements"]  #array of root elements: Element is composed of: name, percent
tree = parsed_response["tree"]  #composed of: name, size, children

sunburst_response_file.close()
del sunburst_response_file
del sunburst_response
del parsed_response

# len(tree.children) == len(elements) - 1 => we don't consider "END_PATH" in the former
# let's check
assert(len(elements) == len(tree["children"]) + 1)
percents = list(map(lambda x: x["percent"], elements))
assert(sum(percents) == 1.0)
del percents


root_node = tree
del tree
first_level = root_node["children"]

sizes = list(map(lambda x: x["size"], first_level))
assert(sum(sizes) == root_node["size"])

print("finished")