with open("demofile.txt") as f: # Read the content
  for a in f:
    print(a)

with open("demofile.txt", "a") as f: # Write new content (a = append)
  f.write("Hello World!\n")