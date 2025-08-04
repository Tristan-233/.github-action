import os
import re
os.chdir(os.path.dirname(__file__))
import requests
import subprocess
from urllib.parse import urlparse

#
token = os.environ["GITHUB_TOKEN"]
repo = os.environ["GITHUB_REPO"]
branch = os.environ["GITHUB_BRANCH"]
username = os.environ["GITHUB_AUTHOR"]

print(branch)
print(username)
print(repo)

url = f"https://api.github.com/repos/{repo}/commits?sha={branch}"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json",
}

res = requests.get(url, headers=headers)
if res.status_code == 200:
    commit_sha1 = os.environ["GITHUB_COMMIT_SHA1"]
    print(f"Latest commit SHA for branch '{username}': {commit_sha1}")
else:
    print(f"Failed to get commit SHA: {res.status_code}")
    print(res.text)
    exit(1)

plan_name = f" {username}-{commit_sha1}"
jenkins_url = "https://10.1.127.226/job/RD_Selftest/buildWithParameters"
jenkins_token = "12345678901234"
params = {
    "token": jenkins_token
}
data = {
    "PLAN_NAME": plan_name
}

res = requests.post(
    jenkins_url,
    auth=("atse", "11793945a21a758077b07479de61030a0e"),  # API token
    params=params,
    data=data,
    verify=False
)

if res.status_code == 201:
    print(f"Jenkins job triggered with PLAN_NAME={plan_name}")
else:
    print(f"Failed: {res.status_code}")
    print(res.text)