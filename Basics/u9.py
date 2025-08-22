print("Input file name")
file_name = input()

try:
    with open(file_name) as f: # Read the content
        for a in f:
            print(a)

    with open(file_name, "a") as f: # Write new content (a = append)
        f.write("Hello World!\n")

except FileNotFoundError:
    print("Error fetching file")
except:
    print("Unkown error")
    


