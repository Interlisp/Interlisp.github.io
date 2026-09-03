#!/bin/bash
# File: deploy-search-function.sh

PROJECT_ID="interlispsearch"
REGION="us-central1"
WEBSITE_ENGINE_ID="interlisp-website-only"   # [interlisp-web-sites_1741606671710] — proven www history/medley (SUCCEEDED)
GITHUB_ENGINE_ID="interlisp-github-only"     # [interlisp-github-v2] — issues/PRs/discussions
# Fallback unified engine retained for single-engine callers but not used by dual-fetch:
FALLBACK_ENGINE_ID="interlisp-search-unified" # [interlisp-web-sites_1741606671710, interlisp-github-v2]
# Verify engines exist (REST, no gcloud discoveryengine):
# TOKEN=$(gcloud auth application-default print-access-token); curl -s -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: interlispsearch" "https://discoveryengine.googleapis.com/v1/projects/interlispsearch/locations/global/collections/default_collection/engines" | python3 -m json.tool | grep -E '"name"|interlisp-website-only|interlisp-github-only'

echo "Deploying search function to $REGION..."
echo "WEBSITE_ENGINE_ID=$WEBSITE_ENGINE_ID GITHUB_ENGINE_ID=$GITHUB_ENGINE_ID (fallback $FALLBACK_ENGINE_ID)"
echo ""

gcloud functions deploy search \
  --gen2 \
  --runtime=nodejs24 \
  --region=$REGION \
  --source=. \
  --entry-point=search \
  --trigger-http \
  --allow-unauthenticated \
  --service-account=vertex-search-sa@interlispsearch.iam.gserviceaccount.com \
  --set-env-vars PROJECT_ID=$PROJECT_ID,WEBSITE_ENGINE_ID=$WEBSITE_ENGINE_ID,GITHUB_ENGINE_ID=$GITHUB_ENGINE_ID,ENGINE_ID=$WEBSITE_ENGINE_ID \
  --memory=256Mi \
  --timeout=30s \
  --project=$PROJECT_ID

echo ""
echo "Deployed: https://$REGION-$PROJECT_ID.cloudfunctions.net/search"
echo "Env: WEBSITE_ENGINE_ID=$WEBSITE_ENGINE_ID GITHUB_ENGINE_ID=$GITHUB_ENGINE_ID ENGINE_ID=$WEBSITE_ENGINE_ID (fallback $FALLBACK_ENGINE_ID kept as engine)"
