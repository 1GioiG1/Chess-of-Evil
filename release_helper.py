import os, json, time, sys

try:
    import requests
except ImportError:
    os.system(f"{sys.executable} -m pip install requests -q")
    import requests

token = os.environ["GITHUB_TOKEN"]
repo  = os.environ["GITHUB_REPOSITORY"]
tag   = os.environ["TAG_NAME"]
api   = f"https://api.github.com/repos/{repo}"

s = requests.Session()
s.headers.update({
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
})

# Delete existing release if present
r = s.get(f"{api}/releases/tags/{tag}")
if r.status_code == 200:
    rid = r.json()["id"]
    print(f"Deleting release {rid}...")
    s.delete(f"{api}/releases/{rid}")
    time.sleep(2)

# Create release
body = f"## Chess of Evil {tag}\n\n- **Windows**: Chess_of_Evil.exe\n- **Linux**: Chess_of_Evil_Linux\n- **Source**: main.py"
r = s.post(f"{api}/releases", json={
    "tag_name": tag,
    "name": f"Chess of Evil {tag}",
    "body": body,
    "draft": False,
    "prerelease": False,
    "make_latest": "true",
})
print(f"Create release: {r.status_code}")
if r.status_code != 201:
    print(r.text)
    sys.exit(1)

upload_url = r.json()["upload_url"].split("{")[0]
print(f"Upload URL: {upload_url}")

files_to_upload = [
    ("release/Chess_of_Evil.exe",   "Chess_of_Evil.exe",   "application/octet-stream"),
    ("release/Chess_of_Evil_Linux", "Chess_of_Evil_Linux",  "application/octet-stream"),
    ("main.py",                     "main.py",              "text/x-python"),
]

for path, name, mime in files_to_upload:
    if not os.path.exists(path):
        print(f"SKIP {name}")
        continue
    size = os.path.getsize(path)
    print(f"Uploading {name} ({size//1024}KB)...")
    with open(path, "rb") as f:
        up = requests.post(
            f"{upload_url}?name={name}",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": mime,
                "Accept": "application/vnd.github+json",
            },
            data=f,
            timeout=300,
        )
    if up.status_code in (200, 201):
        print(f"  OK {name}")
    else:
        print(f"  WARN {name}: {up.status_code} {up.text[:200]}")

print("Done!")
