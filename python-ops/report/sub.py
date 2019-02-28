import subprocess


def update():
	
	p = subprocess.Popen("apt-get update",shell=True, stdout=subprocess.PIPE)
	p.wait()
	out = p.communicate()
	print out

update()
