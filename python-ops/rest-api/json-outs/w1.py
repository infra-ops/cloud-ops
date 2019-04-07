import winrm

s = winrm.Session('192.168.0.118', auth=('nik', 'iis123'))
r = s.run_cmd('ipconfig', ['/all'])