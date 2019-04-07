from ansible_vault import Vault
#from CorrectPythonPackage.token import *


vault = Vault('tower@123')
data = vault.dump(vault, open('vault.yml', 'w'))

# also you can get encrypted text
print(vault.dump(data))


