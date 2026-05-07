import os, json, time, sys, subprocess

try:
    import requests
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"])
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
release_id = r.json()["id"]
print(f"Release ID: {release_id}")

# Upload files via curl (much more reliable for large files)
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
    print(f"Uploading {name} ({size//1024}KB) via curl...")
    
    result = subprocess.run([
        "curl", "-sS",
        "--max-time", "600",
        "--retry", "3",
        "--retry-delay", "5",
        "-X", "POST",
        "-H", f"Authorization: Bearer {token}",
        "-H", f"Content-Type: {mime}",
        "-H", "Accept: application/vnd.github+json",
        "--data-binary", f"@{path}",
        f"{upload_url}?name={name}"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        try:
            resp_json = json.loads(result.stdout)
            if "id" in resp_json:
                print(f"  OK {name} (asset id: {resp_json['id']})")
            else:
                print(f"  WARN {name}: {result.stdout[:200]}")
        except Exception:
            print(f"  OK {name}")
    else:
        print(f"  ERROR {name}: {result.stderr[:200]}")

print("Done!")
