import os
import boto.ec2
#import boto3
import datetime
import argparse


parser = argparse.ArgumentParser (description='script for checking AWS Ins')
parser.add_argument ('-l','--location',dest='location',default='us-east-1',help="location of aws isntance, default is us-east-1")
parser.add_argument ('-s','--state',dest='state',required=True,help="should be running or stopped")
result = parser.parse_args()

location = result.location
state = result.state 

if state != 'running' and state != 'stopped':
	print "-s | --state should be running || stopped" 
	quit()

current_time = datetime.datetime.now()
current_time_string = current_time.strftime("%d-%b-%Y-%H-%M")
script = os.path.basename(__file__)

conn=boto.ec2.connect_to_region(location)
reservations = conn.get_all_instances()

all_inst = []
list_running = []
def running_instance (res):
	for res in reservations:
		for inst in res.instances:
			if 'Name' in inst.tags:
				Required_Filed = ','.join([inst.tags['Name'], inst.id, inst.state])
				all_inst.append(Required_Filed)
#			else:
#				print inst.id, inst.state
	return all_inst

running_instance(reservations)

for lists in all_inst:
	if state in lists:
		all_run = lists.split(",")
		running_only = all_run[0] + "\t" + all_run[1]
		list_running.append(running_only)
print script + "\t" + location + "\t" + state
for l in list_running:
	print l
#
#print "\n" + script + "us-east-1\tstopped"
#for l in list_stop:
#	print l
##for res in reservations:
##   for inst in res.instances:
##        if 'Name' in inst.tags:
##            print "%s (%s) [%s]" % (inst.tags['Name'], inst.id, inst.state)
##        else:
##            print "%s [%s]" % (inst.id, inst.state)
##            f2 = open('status'+current_time_string+'.txt', 'a')
##            f2.write(inst.id)
##            f2.close()



