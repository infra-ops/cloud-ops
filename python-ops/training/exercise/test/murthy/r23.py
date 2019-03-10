file_read = open("/home/matrix/Desktop/python_scripts/text_process1/test11",'r')
file_write = open("/home/matrix/Desktop/python_scripts/text_process1/test11_new",'w')
counter = 1
lines = file_read.readlines()
for line in lines:
file_write.write(str(counter)+ " " +line)
counter += 1

file_write.close()
file_read.close()