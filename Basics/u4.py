family_members = []
is_running = True

while is_running:
    print("Enter name:")
    name = input()
    if name == "slut":
        is_running = False
        print("Enter a name to search:")
        search = input()
        found = False
        if name in family_members:
            print("User found")
        else:
            print("User not found")      
    else:
        family_members.append(name)
