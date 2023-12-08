# генерация списка портов для torcc файла
file = open("ports.txt", "w+")

for i in range(8000, 9150):
    file.write("\nSocksPort " + str(i))