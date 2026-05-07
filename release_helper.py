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

# ── Push .exe to 'releases' branch ──────────────────────────────
print("Pushing exe to releases branch...")

exe_path = "release/Chess_of_Evil.exe"
if os.path.exists(exe_path):
    # Get or create releases branch
    r = s.get(f"{api}/git/ref/heads/releases")
    if r.status_code == 404:
        # Create branch from main
        main = s.get(f"{api}/git/ref/heads/main")
        if main.status_code != 200:
            main = s.get(f"{api}/git/ref/heads/master")
        sha = main.json()["object"]["sha"]
        s.post(f"{api}/git/refs", json={
            "ref": "refs/heads/releases",
            "sha": sha
        })
        print("Created releases branch")

    # Get current file SHA if exists (needed for update)
    r = s.get(f"{api}/contents/Chess_of_Evil.exe",
              params={"ref": "releases"})
    file_sha = r.json().get("sha") if r.status_code == 200 else None

    # Read and encode file
    import base64
    with open(exe_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()

    payload = {
        "message": f"Update exe for {tag}",
        "content": content,
        "branch": "releases",
    }
    if file_sha:
        payload["sha"] = file_sha

    r = s.put(f"{api}/contents/Chess_of_Evil.exe", json=payload)
    if r.status_code in (200, 201):
        print(f"OK Chess_of_Evil.exe pushed to releases branch")
    else:
        print(f"WARN: {r.status_code} {r.text[:300]}")
else:
    print(f"SKIP: {exe_path} not found")

# Also push main.py
for path, name in [("main.py", "main.py")]:
    if not os.path.exists(path):
        continue
    r = s.get(f"{api}/contents/{name}", params={"ref": "releases"})
    file_sha = r.json().get("sha") if r.status_code == 200 else None
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    payload = {"message": f"Update {name} for {tag}", "content": content, "branch": "releases"}
    if file_sha:
        payload["sha"] = file_sha
    r = s.put(f"{api}/contents/{name}", json=payload)
    print(f"{'OK' if r.status_code in (200,201) else 'WARN'} {name}")

# ── Also create/update Release with source code info ────────────
r = s.get(f"{api}/releases/tags/{tag}")
if r.status_code == 200:
    rid = r.json()["id"]
    s.delete(f"{api}/releases/{rid}")
    time.sleep(2)

raw_base = f"https://raw.githubusercontent.com/{repo}/releases"
body = (f"## Chess of Evil {tag}\n\n"
        f"### Скачать / Download\n"
        f"- **Windows**: [{raw_base}/Chess_of_Evil.exe]({raw_base}/Chess_of_Evil.exe)\n"
        f"- **Source**: [{raw_base}/main.py]({raw_base}/main.py)\n\n"
        f"Или скачай [Chess_of_Evil.exe]({raw_base}/Chess_of_Evil.exe) напрямую.")

r = s.post(f"{api}/releases", json={
    "tag_name": tag,
    "name": f"Chess of Evil {tag}",
    "body": body,
    "draft": False,
    "prerelease": False,
    "make_latest": "true",
})
print(f"Release: {r.status_code}")
print("Done!")
