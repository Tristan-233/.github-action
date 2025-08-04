import os
import re
os.chdir(os.path.dirname(__file__))
import requests
import subprocess

token = os.environ["GITHUB_TOKEN"]
remote_url = subprocess.check_output(["git", "remote", "get-url", "origin"], text=True).strip()
match = re.search(r"(github\.com[:/])([^/]+/[^/]+)(?:\.git)?", remote_url)
repo = match.group(2)
branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
username = subprocess.check_output(["git", "log", "-1", "--pretty=format:%an"], text=True).strip()

print(branch)
print(username)
print(repo)

url = f"https://api.github.com/repos/{repo}/commits?sha={branch}"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json",
}
#
res = requests.get(url, headers=headers)
if res.status_code == 200:
    commit_sha1 = subprocess.check_output(
        ["git", "ls-remote", "origin", "HEAD"],
        text=True
    ).split()[0]
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