from ansible.constants import DEFAULT_VAULT_ID_MATCH
from ansible.parsing.vault import VaultLib
from ansible.parsing.vault import VaultSecret

vault = VaultLib([(DEFAULT_VAULT_ID_MATCH, VaultSecret('tower@123'))])
print vault.decrypt(open('/home/nik/Desktop/git-repo/cloud-ops/python-ops/rest-api/json-outs/env-1.json').read())

