import json
import xlwt

f = open('jtest.txt', 'r')

data = f.read()

jsondata = json.loads(data)

workbook = xlwt.Workbook()

sheet = workbook.add_sheet("joutput")

sheet.write(0, 0, 'Value')
sheet.write(0, 1, 'InstanceType')
sheet.write(0, 2, 'PrivateIpAddress')
sheet.write(0, 3, 'PublicIp')

dic = {}
for i in range(len(jsondata['Reservations'])):
    publicip = jsondata['Reservations'][i]['Instances'][0]['PublicIpAddress']
    value = jsondata['Reservations'][i]['Instances'][0]['Tags'][0]['Value']
    insttype = jsondata['Reservations'][i]['Instances'][0]['InstanceType']
    privateip = jsondata['Reservations'][i]['Instances'][0]['NetworkInterfaces'][0]['PrivateIpAddresses'][0]['PrivateIpAddress']
    dic[value] = [value, insttype, privateip, publicip]

values = dic.keys()
values.sort()

k = 1
for i in values:
    sheet.write(k,0, dic[i][0])
    sheet.write(k,1, dic[i][1])
    sheet.write(k,2, dic[i][2])
    sheet.write(k,3, dic[i][3])
    k+=1

workbook.save('joutput.xls')


