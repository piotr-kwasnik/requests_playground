#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""git_server.py
Some simple coding to explore request lib

It is based on:
http://docs.python-requests_playground.org/en/master/user/quickstart/
"""

import requests
import sys
import os
import json


class GitServerApi(object):
    pass


class GitLabApi(GitServerApi):

    """
    Basic GitLab operations
    """
    pass


class GitHubApi(GitServerApi):

    """
    Basic GitHub operations
    """

    def __init__(self, git_user, git_pass, git_url='https://api.github.com'):
        self.git_url = git_url
        self.git_user = git_user
        self.git_pass = git_pass

    def create_repository(self, name, description=''):
        _api_end_point = '/user/repos'

        data = {
            "name": name,
            "description": description,
        }

        headers = {
            "user-agent": self.git_user
        }

        r = requests.post(self.git_url + _api_end_point,
                          auth=(self.git_user, self.git_pass),
                          headers=headers,
                          json=data)

        print(r.headers)

        if r.status_code == 201:
            print('The "{}" repository was created successfully.'.format(name))
        else:
            print(r.json()['message'])

    def delete_repository(self, name):
        _api_end_point = '/repos/' + self.git_user + '/' + name

        r = requests.delete(self.git_url + _api_end_point,
                            auth=(self.git_user, self.git_pass))

        if r.status_code == 204:
            print('The "{}" repository was deleted successfully.'.format(name))

    def list_repositories(self):

        _api_end_point = '/user/repos'

        with requests.Session() as s:
            s.auth = (self.git_user, self.git_pass)
            r = s.get(self.git_url + _api_end_point)

        for repository in r.json():
            print(repository['name'])

        print('\nUser {} has {} repositories!'.format(self.git_user,
                                                      str(len(r.json()))))

    def user_info(self):
        _api_end_point = '/user'
        r = requests.get(self.git_url + _api_end_point,
                         auth=(self.git_user, self.git_pass))

        print(json.dumps(r.json(), indent=2))


def main(argv):

    pk_git = GitHubApi(os.environ['GITHUB_USER'], os.environ['GITHUB_PASS'])

    # pk_git.create_repository('requests_playground')
    # pk_git.delete_repository('')
    pk_git.list_repositories()
    # pk_git.user_info()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
