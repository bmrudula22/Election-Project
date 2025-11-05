import requests
import argparse

# === Step 1: Take inputs from terminal ===
parser = argparse.ArgumentParser(description="GitHub Repo Dashboard")
parser.add_argument("owner", help="GitHub repository owner (e.g., torvalds)")
parser.add_argument("repo", help="GitHub repository name (e.g., linux)")
parser.add_argument("--skip", nargs="*", type=int, default=[], help="PR numbers to skip (optional)")
args = parser.parse_args()

OWNER = args.owner
REPO = args.repo
SKIP_PRS = args.skip

# === Step 2: Get total files and lines of code ===
def get_files_and_lines(owner, repo):
    print(f"Fetching files and line counts for {owner}/{repo} ...")
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
    r = requests.get(url)
    if r.status_code != 200:
        print("❌ Failed to fetch repo data (maybe empty or wrong name).")
        return 0, 0

    data = r.json()
    files = [f['path'] for f in data.get('tree', []) if f['type'] == 'blob']

    total_lines = 0
    for file in files[:10]:  # limit to 10 files for speed
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{file}"
        resp = requests.get(raw_url)
        if resp.status_code == 200:
            total_lines += len(resp.text.splitlines())

    return len(files), total_lines

# === Step 3: Get PR details ===
def get_pr_details(owner, repo, skip_prs):
    print(f"Fetching PR details for {owner}/{repo} ...")
    prs = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&per_page=100&page={page}"
        resp = requests.get(url)
        data = resp.json()
        if not data or 'message' in data:
            break
        prs.extend(data)
        page += 1

    merged_prs = [pr for pr in prs if pr.get('merged_at') and pr['number'] not in skip_prs]
    dev_count = {}
    for pr in merged_prs:
        user = pr['user']['login']
        dev_count[user] = dev_count.get(user, 0) + 1

    return len(merged_prs), dev_count

# === Step 4: Run everything ===
files, lines = get_files_and_lines(OWNER, REPO)
total_prs, devs = get_pr_details(OWNER, REPO, SKIP_PRS)

# === Step 5: Show output ===
print("\n📊 GitHub Repo Summary")
print(f"Total Files: {files}")
print(f"Total Lines of Code: {lines}")
print(f"Total Merged PRs: {total_prs}")

print("\n👩‍💻 Developer Merge Counts:")
for dev, count in devs.items():
    print(f"  {dev:20} -> {count}")