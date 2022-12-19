# 1. blob paths must be same
# 2. update any http paths in the repo json files
# 3. create order is important: blob, repo, content selector, priv, role, , user

import sys
import json
import argparse
import requests
import os
import constants



def app_init():
    global nx_source_server, nx_destination_server, nx_user, nx_pwd, nx_type, nx_run, nx_blobs, datafile

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--sourceserver', help='', required=True)
    parser.add_argument('-d', '--destinationserver', help='', required=True)
    parser.add_argument('-a', '--user', help='', default="admin", required=False)
    parser.add_argument('-p', '--passwd', default="admin123", required=False)
    parser.add_argument('-t', '--type', required=False)
    parser.add_argument('-f', '--datafile', required=False)
    parser.add_argument('-r', '--run', action='store_true')

    args = vars(parser.parse_args())
    
    nx_source_server = args["sourceserver"]
    nx_destination_server = args["destinationserver"]
    nx_user = args["user"]
    nx_pwd = args["passwd"]
    nx_type = args['type']
    nx_run = args['run']
    nx_blobs = False 

    datafile = args['datafile']

    return


def create_object(object_name, type_api, payload):
    url = "{}/{}/{}" . format(nx_destination_server, constants.base_url, type_api)
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

    json_obj_fmt = json.dumps(payload, indent=2)
    print(json_obj_fmt)

    if nx_run:
        print("creating...")
        resp = requests.post(url, 
                            allow_redirects = False,
                            json=payload, 
                            auth=(nx_user, nx_pwd), 
                            verify=False)

        print(resp.status_code)

        if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204:
            # res = resp.json()
            # print('success creating ' + nx_type + ': ' + object_name)
            print('success')
        else:
            # print('error creating ' + nx_type + ': ' + object_name)
            # print(payload)
            # print('error' )
            print(resp)
        
    return


def read_json_file(datafile):
    f = open(datafile)
    data = json.load(f)
    return data


def create_blobs():
    f = constants.output_dir + '/blob.json'
    data = read_json_file(f)

    for blob in data:
        name = blob['name']
        type = blob['type']

        if type == 'File' and not name == constants.ootb_blobstore:

            blobpath_file = constants.output_dir + '/blob_' + name + '.json'
            pathconfig = read_json_file(blobpath_file)
            blob_path = pathconfig['path']

            blob_payload = {}
            blob_payload['softQuota'] = {}
            # blob_payload['softQuota']['type'] = 'File'
            # blob_payload['softQuota']['limt'] = 0
            blob_payload['path'] = blob_path
            blob_payload['name'] = name

            print ('got blob: ' + name + " " + type + " " + blob_path + " " + constants.blobpath_api)
            create_object(name, constants.blobpath_api, blob_payload)
        else:
            print("default blob: " + name  + " [do not create]")

    return


def replace_server_path():
    repo_src = constants.output_dir + '/repo.json'
    repo_dest = constants.output_dir + '/repo_dest.json'

    with open(repo_src, 'r') as fi:
        data = fi.read()
        data = data.replace(nx_source_server, nx_destination_server)

    with open(repo_dest, 'w') as fo:
        fo.write(data)
        fo.close

    return repo_dest

    
def create_repositories():

    f = replace_server_path()
    data = read_json_file(f)

    hosted_repos = get_repos_by_type(data, 'hosted')
    proxy_repos = get_repos_by_type(data, 'proxy')
    group_repo = get_repos_by_type(data, 'group')

    _create_repositories(hosted_repos)
    _create_repositories(proxy_repos)
    _create_repositories(group_repo)

    return


def get_repos_by_type(data, find_type):
    repos = []

    for repo in data:
        type = repo['type']
        if type == find_type:
            repos.append(repo)

    return repos


def _create_repositories(data):
    for repo in data:
        name = repo["name"]
        format = repo["format"]
        # url = repo["url"]
        type = repo["type"]

        if not name in constants.ootb_repositories:
            if format == "maven2":
                format = format[:-1]

            repo_api = "repositories/" + format + "/" + type

            print ('got repository: ' + name + " " + format + " " + repo_api)
            create_object(name, repo_api, repo)
        else:
            print("default repo: " + name  + " [do not create]")

    return


def create_content_selectors():
    nx_type = 'contentselector'
    type_api = constants.endpoints[nx_type]

    f = constants.output_dir + '/contentselector.json'
    data = read_json_file(f)

    for cs in data:
        name = cs['name']
        print ('got content selector: ' + name + " " + type_api)
        create_object(name, type_api, cs)

    return


def create_privileges():
    f = constants.output_dir + '/priv.json'
    data = read_json_file(f)

    for priv in data:
        priv_type = priv["type"]
        priv_name = priv["name"]

        if not priv_name.startswith(constants.ootb_priv):
            type_api = constants.privilege_endpoints[priv_type]
            print('got privilege: ' + priv_name + " " + priv_type + " " + type_api)
            create_object(priv_name, type_api, priv)
        else:
            print("default privilege: " + priv_name + " [do not create]")

    return


def create_roles():
    nx_type = 'role'
    type_api = constants.endpoints[nx_type]

    f = constants.output_dir + '/role.json'
    data = read_json_file(f)

    for role in data:
        role_name = role["name"]

        if not role_name in constants.ootb_roles:
            print('got role: ' + role_name + " " + type_api)
            create_object(role_name, type_api, role)
        else:
            print("default role: " + role_name + " [do not create]")


    return


def create_users():
    nx_type = 'user'
    type_api = constants.endpoints[nx_type]

    f = constants.output_dir + '/user.json'
    data = read_json_file(f)

    for user in data:
        user_name = user["userId"]

        if not user_name in constants.ootb_users:
            print('got user: ' + user_name + " " + type_api)
            create_object(user_name, type_api, user)
        else:
            print("default user: " + user_name + " [do not create]")


    return

def main():
    app_init()

    if nx_blobs:
        create_blobs()

    create_repositories()
    create_content_selectors()
    create_privileges()
    create_roles()
    create_users()


                

if __name__ == '__main__':
    main()
