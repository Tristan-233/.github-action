import os
import requests
import subprocess

# 抓最新 commit 的作者名稱
author_name = subprocess.check_output(
    ["git", "log", "-1", "--pretty=format:%an"],
    text=True
).strip()

print(author_name)
# 從環境變數中取得資訊
token = os.environ['GITHUB_TOKEN']
repo = os.environ['GITHUB_REPO']
branch = os.environ['GITHUB_BRANCH']

url = f"https://api.github.com/repos/{repo}/commits/{branch}"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json",
}

res = requests.get(url, headers=headers)
if res.status_code == 200:
    commit_sha = res.json()["sha"]
    print(f"Latest commit SHA for branch '{branch}': {commit_sha}")
else:
    print(f"Failed to get commit SHA: {res.status_code}")
    print(res.text)
    exit(1)