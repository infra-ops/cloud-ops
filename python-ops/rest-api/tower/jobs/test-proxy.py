def create_key(service_account_email,keyfile,envi,link,token,cred_name,user,proj,idd):
    """Creates a key for a service account."""
#    export https_proxy=http://localhost:3128
    print os.environ.get('https_proxy', 'Not Set') #if theres no var set , this should make an error
    os.environ['https_proxy']='http://localhost:3128' #this changes var
    print os.environ.get('https_proxy', 'Not Set') #this prints the var value
    print "here"
    quit()
