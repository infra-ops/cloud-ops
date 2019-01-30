import sys
from github import Github
from tower_cli import get_resource
from tower_cli.conf import settings
import argparse

import yaml

def create_repo_and_project(token,tower_host,tower_user,tower_pass,cred_id,yml_file,org_name,repo_name):


    github_client = Github(token)


    org = github_client.get_organization(org_name)


    new_repo = org.create_repo(repo_name,repo_name)

    # Create objects and directories
    new_repo.create_file("default/ ", "default file", "",)
    new_repo.create_file("task/ ", "task file", "")
    new_repo.create_file("var/ ", "var file", "")



    with open(yml_file, "rb") as default_file:
        encoded_string = default_file.read()

        new_repo.create_file(yml_file, "yml file ", encoded_string)

    print ("Repo Cretaed!")


    with settings.runtime_values(username=tower_user, password=tower_pass, host=tower_host, verify_ssl=False):
        try:
            org_res = get_resource('organization')
            cred_res = get_resource('credential')
            proj_res = get_resource('project')

            proj_update_resource = get_resource('project_update')

            org = org_res.get(org_name)
            cred = cred_res.get(pk=cred_id)

            scm_url = "https://github.com/{}/{}.git".format(org_name,repo_name)

            args = {
                'name':repo_name,
                'desc':repo_name,
                'organization':org['id'],
                'scm_credential': cred_id,
                'scm_branch':'master',
                'scm_type':'git',
                'scm_url':scm_url
            }

            proj = proj_res.create(**args)

            print ("Project Created!!")

        except Exception,e:
            print('Failed with Error: {} '.format(str(e)))

    print ("Repo and Project Created!! ")


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', help='Input file', required=True)
    args = parser.parse_args()
    print (args)
    dict  = yaml.load(open(args.input_file))
    create_repo_and_project(dict['token'],dict['tower_host'],dict['tower_user'],dict['tower_pass'],dict['scm_cred'],dict['role_name'],dict['org_name'],dict['repo_name'])

