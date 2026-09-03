#!/bin/bash
# File: test-citations.sh

FUNCTION_URL="https://us-central1-interlispsearch.cloudfunctions.net/search"

echo "Testing citation preference..."
echo ""

# Test 1: General query (should cite interlisp.org first)
echo "Test 1: Query 'interlisp' (should cite website first)"
echo "=========================================="
curl -s "$FUNCTION_URL?q=interlisp&pageSize=10" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('summary') and data['summary'].get('citations'):
    for i, citation in enumerate(data['summary']['citations'][:3], 1):
        print(f\"[{i}] {citation.get('title', 'Untitled')}\")
        print(f\"    URI: {citation.get('uri', 'N/A')}\")
        print()
else:
    print('No citations found')
"
echo ""

# Test 2: Check first result URL
echo "Test 2: First result should be from interlisp.org"
echo "=========================================="
curl -s "$FUNCTION_URL?q=medley&pageSize=5" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('results'):
    result = data['results'][0]
    print(f\"Title: {result.get('title')}\")
    print(f\"URL: {result.get('url')}\")
    print(f\"Source: {result.get('source')}\")
    print(f\"Priority: {result.get('priority')}\")
else:
    print('No results found')
"
echo ""

# Test 3: Verify GitHub content still appears
echo "Test 3: GitHub content should still appear in results"
echo "=========================================="
curl -s "$FUNCTION_URL?q=github&pageSize=20" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('results'):
    github_results = [r for r in data['results'] if 'github' in r.get('url', '')]
    print(f\"Found {len(github_results)} GitHub results\")
    for r in github_results[:2]:
        print(f\"  - {r.get('title')}\")
        print(f\"    {r.get('url')}\")
else:
    print('No results found')
"
