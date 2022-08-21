#!/usr/bin/env python3
# This was used to generate the list of grandfathered allowed messages in html_validate_test

import json
import subprocess

p = subprocess.run(["vnu", "--skip-non-html", "--errors-only", "--exit-zero-always", "--format", "json", "public/"], capture_output=True)

messages = json.loads(p.stderr)['messages']
allowed_messages = set(message['message'] for message in messages)

for m in sorted(allowed_messages):
  print(m)
