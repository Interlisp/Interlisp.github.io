'use strict';

const { GoogleAuth } = require('google-auth-library');
const { Storage } = require('@google-cloud/storage');

const PROJECT_ID = 'interlispsearch';
const LOCATION = 'global';
// Structured GitHub store — NOT the website store. Keeps website crawl separate
// and is consumed via interlisp-github-only engine (blended 70/30 in search function).
// Fallback engine interlisp-search-unified ([interlisp-web-sites_1741606671710, interlisp-github-v2]) retained.
const DATA_STORE_ID = 'interlisp-github-v2';
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const GITHUB_ORG = 'Interlisp';
const GITHUB_REPOS = ['medley', 'maiko', 'Interlisp.github.io'];

const auth = new GoogleAuth({
  scopes: ['https://www.googleapis.com/auth/cloud-platform']
});

const storage = new Storage({ projectId: PROJECT_ID });

exports.reimportGithub = async (message, context) => {
  console.log(`[${new Date().toISOString()}] Starting GitHub reimport...`);
  
  try {
    // 1. Fetch GitHub content
    const gitHubDocuments = [];
    
    console.log('Fetching GitHub Issues...');
    const issues = await fetchGitHubIssues();
    gitHubDocuments.push(...issues);
    console.log(`Fetched ${issues.length} GitHub issues`);
    
    console.log('Fetching GitHub Pull Requests...');
    const prs = await fetchGitHubPullRequests();
    gitHubDocuments.push(...prs);
    console.log(`Fetched ${prs.length} GitHub pull requests`);
    
    console.log('Fetching GitHub Markdown files...');
    const markdownFiles = await fetchGitHubMarkdown();
    gitHubDocuments.push(...markdownFiles);
    console.log(`Fetched ${markdownFiles.length} GitHub markdown files`);
    
    if (gitHubDocuments.length === 0) {
      console.warn('No GitHub documents fetched. Check GitHub token and repo access.');
      return { status: 'NO_DOCUMENTS', count: 0 };
    }
    
    // 2. Convert to JSONL format — interlisp-github-v2 is NO_CONTENT: each line is
    // {id, structData:{...}} with sanitized id ^[a-zA-Z0-9-_]+$ on branches/0 (see guide 1.6).
    const sanitizeId = (id) => id.replace(/\./g, '-').replace(/[^a-zA-Z0-9-_]/g, '-');
    console.log(`Converting ${gitHubDocuments.length} documents to JSONL (structData, branches/0, sanitized ids)...`);
    const jsonlLines = gitHubDocuments.map(doc => {
      const rawId = doc.id;
      const sid = sanitizeId(rawId);
      // Flatten metadata into structData as expected by the structured store
      const m = doc.metadata || {};
      const structData = {
        id: sid,
        title: doc.title || '',
        url: doc.url || '',
        content: doc.content || '',
        source: m.source || 'github',
        priority: m.priority || 3,
        type: m.content_type || m.type || null,
        content_type: m.content_type || null,
        repo: m.repo || null,
        state: m.state || null,
        number: m.issue_number || m.pr_number || m.number || null,
        issue_number: m.issue_number || null,
        pr_number: m.pr_number || null,
        file: m.file || null,
        created_at: m.created_date || null,
        updated_at: m.updated_date || null,
        created_date: m.created_date || null,
        updated_date: m.updated_date || null,
        last_indexed: m.last_indexed || new Date().toISOString()
      };
      // Remove nulls to keep JSONL clean
      Object.keys(structData).forEach(k => structData[k] == null && delete structData[k]);
      return JSON.stringify({ id: sid, structData });
    });
    const jsonlContent = jsonlLines.join('\n');
    
    // 3. Upload JSONL to Cloud Storage
    const bucketName = `${PROJECT_ID}-search-imports`;
    const fileName = `github-import-${Date.now()}.jsonl`;
    
    console.log(`Creating Cloud Storage bucket if needed: ${bucketName}`);
    const bucket = storage.bucket(bucketName);
    
    try {
      await bucket.exists();
    } catch (e) {
      console.log(`Creating bucket: ${bucketName}`);
      await storage.createBucket(bucketName, { location: 'US' });
    }
    
    console.log(`Uploading JSONL to gs://${bucketName}/${fileName}`);
    const file = bucket.file(fileName);
    await file.save(jsonlContent);
    
    // 4. Call Vertex AI importDocuments API
    const client = await auth.getClient();
    const token = await client.getAccessToken();
    
    const importUrl = `https://discoveryengine.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/collections/default_collection/dataStores/${DATA_STORE_ID}/branches/0/documents:import`;
    
    console.log(`Calling Vertex AI import API: ${importUrl}`);
    
    const importResponse = await fetch(importUrl, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token.token}`,
        'Content-Type': 'application/json',
        'x-goog-user-project': PROJECT_ID
      },
      body: JSON.stringify({
        gcsSource: {
          inputUris: [`gs://${bucketName}/${fileName}`]
        }
      })
    });
    
    if (!importResponse.ok) {
      const errorText = await importResponse.text();
      throw new Error(`Import failed: ${importResponse.statusText} - ${errorText}`);
    }
    
    const importData = await importResponse.json();
    console.log(`Import operation started: ${importData.name}`);
    console.log(`[${new Date().toISOString()}] GitHub reimport completed successfully`);
    
    return {
      status: 'SUCCESS',
      documentsImported: gitHubDocuments.length,
      operation: importData.name,
      gcsLocation: `gs://${bucketName}/${fileName}`
    };
    
  } catch (err) {
    console.error(`[${new Date().toISOString()}] GitHub reimport error:`, err);
    throw err;
  }
};

async function fetchGitHubIssues() {
  const issues = [];
  
  for (const repo of GITHUB_REPOS) {
    try {
      const url = `https://api.github.com/repos/${GITHUB_ORG}/${repo}/issues?state=all&per_page=100`;
      const response = await fetch(url, {
        headers: {
          'Authorization': `token ${GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json'
        }
      });
      
      if (!response.ok) {
        console.warn(`Failed to fetch issues from ${GITHUB_ORG}/${repo}: ${response.statusText}`);
        continue;
      }
      
      const repoIssues = await response.json();
      
      for (const issue of repoIssues) {
        issues.push({
          id: `github-issue-${repo}-${issue.number}`,
          title: issue.title,
          url: issue.html_url,
          content: issue.body || '',
          metadata: {
            source: 'github',
            priority: 3,
            content_type: 'issue',
            repo: `${GITHUB_ORG}/${repo}`,
            issue_number: issue.number,
            state: issue.state,
            created_date: issue.created_at,
            updated_date: issue.updated_at,
            last_indexed: new Date().toISOString()
          }
        });
      }
    } catch (err) {
      console.error(`Error fetching issues from ${GITHUB_ORG}/${repo}:`, err.message);
    }
  }
  
  return issues;
}

async function fetchGitHubPullRequests() {
  const prs = [];
  
  for (const repo of GITHUB_REPOS) {
    try {
      const url = `https://api.github.com/repos/${GITHUB_ORG}/${repo}/pulls?state=all&per_page=100`;
      const response = await fetch(url, {
        headers: {
          'Authorization': `token ${GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json'
        }
      });
      
      if (!response.ok) {
        console.warn(`Failed to fetch PRs from ${GITHUB_ORG}/${repo}: ${response.statusText}`);
        continue;
      }
      
      const repoPrs = await response.json();
      
      for (const pr of repoPrs) {
        prs.push({
          id: `github-pr-${repo}-${pr.number}`,
          title: pr.title,
          url: pr.html_url,
          content: (pr.body || '') + '\n' + (pr.title || ''),
          metadata: {
            source: 'github',
            priority: 3,
            content_type: 'pull_request',
            repo: `${GITHUB_ORG}/${repo}`,
            pr_number: pr.number,
            state: pr.state,
            created_date: pr.created_at,
            updated_date: pr.updated_at,
            last_indexed: new Date().toISOString()
          }
        });
      }
    } catch (err) {
      console.error(`Error fetching PRs from ${GITHUB_ORG}/${repo}:`, err.message);
    }
  }
  
  return prs;
}

async function fetchGitHubMarkdown() {
  const markdownFiles = [];
  
  for (const repo of GITHUB_REPOS) {
    try {
      // Fetch README
      const readmeUrl = `https://api.github.com/repos/${GITHUB_ORG}/${repo}/readme`;
      const readmeResponse = await fetch(readmeUrl, {
        headers: {
          'Authorization': `token ${GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3.raw'
        }
      });
      
      if (readmeResponse.ok) {
        const content = await readmeResponse.text();
        markdownFiles.push({
          id: `github-markdown-${repo}-README`,
          title: `${repo} README`,
          url: `https://github.com/${GITHUB_ORG}/${repo}/blob/main/README.md`,
          content: content,
          metadata: {
            source: 'github',
            priority: 3,
            content_type: 'markdown',
            repo: `${GITHUB_ORG}/${repo}`,
            file: 'README.md',
            last_indexed: new Date().toISOString()
          }
        });
      }
    } catch (err) {
      console.warn(`No README found in ${GITHUB_ORG}/${repo}`);
    }
  }
  
  return markdownFiles;
}
