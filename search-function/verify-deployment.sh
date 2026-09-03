#!/bin/bash
# File: verify-deployment.sh

PROJECT_ID="interlispsearch"
REGION="us-central1"

echo "Verifying Cloud Function deployment..."
echo ""

gcloud functions describe search \
  --gen2 \
  --region=$REGION \
  --project=$PROJECT_ID \
  --format=json | python3 -m json.tool

echo ""
echo "Function URL: https://$REGION-$PROJECT_ID.cloudfunctions.net/search"
echo ""
echo "Testing function with sample query..."
curl -s "https://$REGION-$PROJECT_ID.cloudfunctions.net/search?q=interlisp&pageSize=5" \
  | python3 -m json.tool | head -50
