family_members = []
is_running = True

while is_running:
    print("Enter name:")
    name = input()
    if name == "slut":
        is_running = False
        for member in family_members:
            print(member)
    else:
        family_members.append(name)
