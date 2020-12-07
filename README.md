### Bitbucket Repository Importer

Bitbucket allows importing repositories from another provider, however it doesn't seem to provide an API for this; when there's multiple repositories to migrate
into Bitbucket this becomes very time consuming.

This script will take a list of source git repositories and then using the Bitbucket API create an empty repository with the same name, then clone the source repo and push all refs to the new Bitbucket remote.

### Usage

Ensure all requirements are met `requirements.txt`.

Populate `config.yml` with credentials and a repository list.

To run:
```
python3 duplicate_repos.py
```

If the source repositories require authentication, this can be included as part of the URL's, for example:

```
https://letmein:secretpassword@repodomain.com/repo/here.git
```

### Credentials

Your bitbucket username can be obtained here:

https://bitbucket.org/account/settings/


An App Password can be obtained by following this documentation, this is your "Token"

https://support.atlassian.com/bitbucket-cloud/docs/app-passwords/

### Config 

`source_repos` in `config.yml` should contain full clone-able URL's (usually ending `.git`)