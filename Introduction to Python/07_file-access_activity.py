file = open("devices.txt", "a")
while True:
    newItem = input("Enter device name: ")
    if newItem == "exit":
        break

    file.write(newItem + "\n")
file.close()
print("All done")
