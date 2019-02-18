import os
import fnmatch

print("Running")
test_path = "D:\\Documents\\autem\\tests\\simulations"
for root, dir, files in os.walk(test_path):
        print(root)
        print("")
        for items in fnmatch.filter(files, "outline.csv"):
                print("..." + items)
        print("")

def simulation_paths(root_path):
    paths = [root for root, dir, files in os.walk(test_path) if any(fnmatch.filter(files, "outline.csv"))]
    return paths

print("Func")
for path in simulation_paths(test_path):
    print(path)