import base64
import os
from datetime import datetime

import requests


def calculate_uptime(birth_date_str):
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
    now = datetime.now()

    years = now.year - birth_date.year
    months = now.month - birth_date.month
    days = now.day - birth_date.day

    if days < 0:
        months -= 1
        days += 30
    if months < 0:
        years -= 1
        months += 12

    return f"{years} years, {months} months, {days} days"


with open("tux-logo2.svg", "rb") as f:
    tux_base64 = base64.b64encode(f.read()).decode()

QUERY = """
query($username: String!) {
  user(login: $username) {
    followers { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER) {
      totalCount
      nodes {
        stargazerCount
        defaultBranchRef {
          target {
            ... on Commit {
              history { totalCount }
            }
          }
        }
      }
    }
  }
}
"""


def fetch_stats(username, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": QUERY, "variables": {"username": username}},
        headers=headers,
    )

    if response.status_code != 200 or "errors" in response.json():
        print("API Error:", response.json())
        return 0, 0, 0, 0

    data = response.json()["data"]["user"]
    followers = data["followers"]["totalCount"]
    repos = data["repositories"]["totalCount"]
    stars = sum(repo["stargazerCount"] for repo in data["repositories"]["nodes"])
    commits = sum(
        repo["defaultBranchRef"]["target"]["history"]["totalCount"]
        for repo in data["repositories"]["nodes"]
        if repo["defaultBranchRef"]
    )
    return followers, repos, stars, commits


def generate_svg(username, followers, repos, stars, commits, tux_base64, uptime_str):
    svg_content = f"""<svg fill="none" width="800" height="820" xmlns="http://www.w3.org/2000/svg">
  <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <style>
        .window {{
          background-color: #0d1117;
          border: 1px solid #30363d;
          border-radius: 12px;
          padding: 0;
          font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
          color: #e6edf3;
          font-size: 14px;
          line-height: 1.5;
          box-shadow: 0 12px 32px rgba(0,0,0,0.6);
          overflow: hidden;
        }}
        .titlebar {{
          background-color: #161b22;
          padding: 10px 16px;
          display: flex;
          align-items: center;
          border-bottom: 1px solid #21262d;
        }}
        .dots {{
          display: flex;
          gap: 8px;
        }}
        .dot {{
          width: 12px;
          height: 12px;
          border-radius: 50%;
        }}
        .dot-red {{ background-color: #ff5f56; }}
        .dot-yellow {{ background-color: #ffbd2e; }}
        .dot-green {{ background-color: #27c93f; }}
        .title {{
          flex-grow: 1;
          text-align: center;
          color: #8b949e;
          font-size: 13px;
          margin-right: 52px;
          font-weight: 500;
        }}
        .body {{
          padding: 24px;
        }}
        .header-row {{
          display: flex;
          align-items: center;
          padding-bottom: 16px;
        }}
        .ascii-col {{
          width: 240px;
          display: flex;
          justify-content: center;
          align-items: center;
        }}
        .info-col {{
          flex-grow: 1;
          padding-left: 20px;
        }}
        .user-title {{
          color: #ffffff;
          font-size: 18px;
          font-weight: bold;
          text-decoration: underline;
          text-underline-offset: 4px;
        }}
        .subtitle-main {{
          color: #e6edf3;
          font-size: 13.5px;
          margin-top: 6px;
        }}
        .subtitle-tags {{
          color: #8b949e;
          font-size: 12.5px;
          margin-bottom: 14px;
        }}

        /* Flexbox Leader Lines */
        .row {{
          display: flex;
          align-items: baseline;
        }}
        .row::after {{
          content: "";
          flex-grow: 1;
          order: 2;
          margin: 0 8px;
          border-bottom: 2px dotted #383e47;
          position: relative;
          top: -3px;
        }}
        .label {{
          color: #ff9f43;
          font-weight: 500;
          order: 1;
          white-space: nowrap;
        }}
        .val {{
          color: #61dafb;
          order: 3;
          white-space: nowrap;
        }}
        .val-highlight {{
          color: #a8e063;
          font-weight: bold;
          order: 3;
          white-space: nowrap;
        }}

        .section-title {{
          color: #b8c0cc;
          margin-top: 14px;
          margin-bottom: 4px;
          font-weight: 500;
        }}

        /* 2x2 Grid Layout for GitHub Stats */
        .stats-grid {{
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 4px 24px;
        }}
      </style>

      <div class="window">
        <div class="titlebar">
          <div class="dots">
            <div class="dot dot-red"></div>
            <div class="dot dot-yellow"></div>
            <div class="dot dot-green"></div>
          </div>
          <div class="title">samyak@openSUSE</div>
        </div>
        <div class="body">
          <!-- Top Side-by-Side Block (Tux + System Info) -->
          <div class="header-row">
            <div class="ascii-col">
              <img
                  src="data:image/svg+xml;base64,{tux_base64}"
                  style="width:185px;height:185px;object-fit:contain;"
              />
            </div>
            <div class="info-col">
              <div class="user-title">samyak@openSUSE</div>
              <div class="subtitle-main">M.Tech Computer Science Student</div>
              <div class="subtitle-tags">Linux • Networking • Security</div>

              <div class="row"><span class="label">OS:</span><span class="val">openSUSE Tumbleweed</span></div>
              <div class="row"><span class="label">Uptime:</span><span class="val">{uptime_str}</span></div>
              <div class="row"><span class="label">Host:</span><span class="val">NIT Karnataka</span></div>
              <div class="row"><span class="label">Kernel:</span><span class="val">Linux 7.1.4</span></div>
              <div class="row"><span class="label">Shell:</span><span class="val">bash 5.3.15</span></div>
              <div class="row"><span class="label">IDE:</span><span class="val">IDEA 2026.2.0, VS Code 1.129.1</span></div>
            </div>
          </div>

          <!-- Bottom Full-Width Sections -->
          <div class="section-title">- Languages -----------------------------------------------------------------------------</div>
          <div class="row"><span class="label">Languages.Programming</span><span class="val">Java, C++, C, Python</span></div>
          <div class="row"><span class="label">Languages.Scripting</span><span class="val">Bash</span></div>
          <div class="row"><span class="label">Languages.Markup</span><span class="val">LaTeX, Markdown</span></div>

          <div class="section-title">- Tools &amp; Frameworks --------------------------------------------------------------------</div>
          <div class="row"><span class="label">Tools.Dev</span><span class="val">Git, GitHub, GitLab, Docker</span></div>
          <div class="row"><span class="label">Tools.Networking</span><span class="val">OpenSSL, NetBird, tcpdump, Wireshark</span></div>
          <div class="row"><span class="label">Tools.Linux</span><span class="val">Network Namespaces, iproute2, systemd</span></div>

          <div class="section-title">- Projects ------------------------------------------------------------------------------</div>
          <div class="row"><span class="label">Projects.Current</span><span class="val">Securing Ethernet Switches</span></div>
          <div class="row"><span class="label">Projects.OpenSource</span><span class="val">NeST - Mutual TLS Support</span></div>
          <div class="row"><span class="label">Projects.Networking</span><span class="val">TLS Handshake (Linux NetNS)</span></div>
          <div class="row"><span class="label">Projects.Security</span><span class="val">IEC 62443 Threat Modeling</span></div>

          <div class="section-title">- Contact -------------------------------------------------------------------------------</div>
          <div class="row"><span class="label">Contact.Email</span><span class="val">samyakgedam03@gmail.com</span></div>
          <div class="row"><span class="label">Contact.LinkedIn</span><span class="val">linkedin.com/in/samyak-gedam/</span></div>
          <div class="row"><span class="label">Contact.GitHub</span><span class="val">github.com/Samyak05</span></div>

          <div class="section-title">- GitHub Stats --------------------------------------------------------------------------</div>
          <div class="stats-grid">
            <div class="row"><span class="label">GitHub.Repositories</span><span class="val-highlight">{repos}</span></div>
            <div class="row"><span class="label">GitHub.Stars</span><span class="val-highlight">{stars}</span></div>
            <div class="row"><span class="label">GitHub.Commits</span><span class="val-highlight">{commits}</span></div>
            <div class="row"><span class="label">GitHub.Followers</span><span class="val-highlight">{followers}</span></div>
          </div>
        </div>
      </div>
    </div>
  </foreignObject>
</svg>
"""
    with open("github-profile.svg", "w") as f:
        f.write(svg_content)
    print("Successfully generated github-profile.svg")


if __name__ == "__main__":
    token = os.getenv("GH_TOKEN")
    username = os.getenv("GH_USERNAME", "Samyak05")

    uptime_str = calculate_uptime("2003-03-11")

    if not token:
        print("Error: GH_TOKEN environment variable is missing.")
    else:
        followers, repos, stars, commits = fetch_stats(username, token)
        generate_svg(
            username, followers, repos, stars, commits, tux_base64, uptime_str
        )