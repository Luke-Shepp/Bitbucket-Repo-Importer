import requests
import yaml
from git import Repo
import tempfile
import shutil

def mirror_repository(source_url, destination_url):
    repo_dir = tempfile.mkdtemp()

    repo = Repo.clone_from(source_url, repo_dir)

    remote = repo.create_remote('bitbucket', url = destination_url)
    remote.push(refspec='refs/remotes/origin/*:refs/heads/*')

    shutil.rmtree(repo_dir)

    print("\tPushed to " + destination_url)

def get_repo_name(repo_url):
    url_parts = repo_url.split('/')
    return url_parts[-1].replace('.git', '')

def load_config():
    with open('config.yml', 'r') as stream:
        try:
            print("Loading config...")
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit()

def create_bitbucket_repo(repo_name, config):
    api_url = config['api'] + "repositories/" + config['workspace'] + "/" + repo_name

    data = {
        'scm': 'git',
        'name': repo_name,
        'project': {
            'key': config['project']
        },
        'is_private': True
    }

    response = requests.post(url = api_url, json = data, auth = (config['username'], config['token']))

    if (response.status_code != 200):
        print("Non-200 status code when creating " + repo_name)
        print(response.content)
        return ''

    json = response.json()

    for link in json['links']['clone']:
        if link['name'] == 'https':
            print("Created " + repo_name)
            return link['href']

    return ''

def main():
    config = load_config()

    if (config['source_repos'] == None):
        print("Please populate the source_repos list in config.yml with GIT URLs to clone from.")
        exit()

    for source_url in config['source_repos']:
        repo_name = get_repo_name(source_url)

        bitbucket_repo_url = create_bitbucket_repo(repo_name, config["bitbucket"])

        if (bitbucket_repo_url == ''):
            continue

        mirror_repository(source_url, bitbucket_repo_url)

    print("Done!")

main()
