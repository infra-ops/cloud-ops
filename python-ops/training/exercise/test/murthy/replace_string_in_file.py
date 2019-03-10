file1 = open("/home/trainer/Desktop/file1.txt",'r')
content = file1.read()

new_content = content.replace("Murthy", "Gopala")

file_name = "/home/trainer/Desktop/file_" + \
    datetime.datetime.now().strftime("%d-%b-%Y-%H-%M-%S") + ".txt"
    
file2 = open(file_name,'w')
file2.write(new_content)

file2.close()
file1.close()