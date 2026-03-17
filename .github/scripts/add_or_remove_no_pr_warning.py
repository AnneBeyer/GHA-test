import json
import os
import re
import argparse
from github import Github

parser = argparse.ArgumentParser(description="Add or remove no-contribution warning from issue body")
parser.add_argument("--mode", choices=["add", "remove"], help="Whether to add or remove warning")
args = parser.parse_args()

# the following env variables are defined in .github/workflows/not_ready_for_pr_warning.yml
g = Github(os.environ["GITHUB_TOKEN"])
repo = g.get_repo(os.environ["GITHUB_REPO"])
issue = repo.get_issue(number=int(os.environ["ISSUE_NUMBER"]))

body = str(issue.body)

message = (
    "> [!WARNING]\n\n" 
    "> This issue is not yet ready for a PR. If you are interested in contributing to "
    "scikit-learn, please have a look at our [contributing guidelines]"
    "(https://scikit-learn.org/dev/developers/contributing.html), and in particular "
    "the sections for [new contributors]"
    "(https://scikit-learn.org/dev/developers/contributing.html#new-contributors) and " 
    'on the ["Needs triage"]'
    "(https://scikit-learn.org/defv/developers/contributing.html#issues-tagged-needs-triage) "
    "label.\n\n"
)

if args.mode == "add":
    if not body.startswith(message):
        new_body = message + body
        issue.edit(body=new_body)
else:
    has_needs_label = any(label.name.startswith("Needs") for label in issue.labels)
    if has_needs_label:
        if body.startswith(message):
            new_body = body.removeprefix(message)
            issue.edit(body=new_body)