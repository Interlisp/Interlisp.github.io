const fs   = require('fs');
const path = require('path');

const GITHUB_TOKEN = process.env.GITHUB_TOKEN || process.env.GITHUB_PAT || process.env.GH_TOKEN || '';
const ORG          = 'Interlisp';
const OUTPUT_FILE  = path.join(__dirname, '../github-index.jsonl');
const DEBUG        = process.env.DEBUG_GITHUB_INDEX === '1';
const START_TIME   = Date.now();

if (!GITHUB_TOKEN) {
  throw new Error('Missing GitHub token. Set GITHUB_TOKEN, GITHUB_PAT, or GH_TOKEN in the environment.');
}

const headers = {
  'Authorization': `Bearer ${GITHUB_TOKEN}`,
  'Accept':        'application/vnd.github+json',
  'X-GitHub-Api-Version': '2022-11-28'
};

const FETCH_TIMEOUT_MS = 30000;
const FETCH_RETRIES = 2;
const MAX_PAGES_PER_PAGINATION = Number.parseInt(process.env.GITHUB_INDEX_MAX_PAGES || '', 10);
const MAX_RATE_LIMIT_RETRIES = Number.parseInt(process.env.GITHUB_RATE_LIMIT_RETRIES || '6', 10);
const SECONDARY_LIMIT_BASE_WAIT_MS = Number.parseInt(process.env.GITHUB_SECONDARY_LIMIT_BASE_WAIT_MS || '60000', 10);
const SECONDARY_LIMIT_MAX_WAIT_MS = Number.parseInt(process.env.GITHUB_SECONDARY_LIMIT_MAX_WAIT_MS || '900000', 10);

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchWithTimeout(url, options = {}, timeoutMs = FETCH_TIMEOUT_MS) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    return await fetch(url, { ...options, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

async function githubRequest(url, options = {}, label = 'request') {
  let lastError;

  for (let attempt = 0; attempt <= MAX_RATE_LIMIT_RETRIES; attempt += 1) {
    try {
      const response = await fetchWithTimeout(url, options);
      if (response.ok) {
        return response;
      }

      const status = response.status;
      const retryAfter = response.headers.get('retry-after');
      const remainingRaw = response.headers.get('x-ratelimit-remaining');
      const resetRaw = response.headers.get('x-ratelimit-reset');
      const remaining = Number.parseInt(remainingRaw || '', 10);
      const resetEpoch = Number.parseInt(resetRaw || '', 10);

      let waitMs = null;
      let reason = '';

      if (retryAfter) {
        const retryAfterSec = Number.parseInt(retryAfter, 10);
        if (Number.isFinite(retryAfterSec) && retryAfterSec > 0) {
          waitMs = retryAfterSec * 1000;
          reason = `retry-after=${retryAfterSec}s`;
        }
      }

      if (waitMs === null && remaining === 0 && Number.isFinite(resetEpoch)) {
        waitMs = Math.max((resetEpoch * 1000) - Date.now(), 1000);
        reason = `x-ratelimit-reset=${resetEpoch}`;
      }

      if (waitMs === null && (status === 403 || status === 429)) {
        const bodyText = await response.clone().text();
        const mentionsRateLimit = /rate limit|secondary rate limit|abuse/i.test(bodyText);
        if (mentionsRateLimit) {
          // Secondary rate limiting guidance: start at 1 minute, then exponential backoff.
          waitMs = Math.min(
            SECONDARY_LIMIT_BASE_WAIT_MS * (2 ** attempt),
            SECONDARY_LIMIT_MAX_WAIT_MS
          );
          reason = 'secondary-rate-limit-backoff';
        }
      }

      if (waitMs !== null) {
        if (attempt >= MAX_RATE_LIMIT_RETRIES) {
          const exhaustedError = new Error(
            `Rate limit retries exhausted for ${label} (status ${status})`
          );
          exhaustedError.status = status;
          exhaustedError.url = url;
          throw exhaustedError;
        }

        const jitterMs = Math.floor(Math.random() * 1000);
        const totalWaitMs = waitMs + jitterMs;
        console.warn(
          `Rate limited for ${label} (status ${status}, ${reason}). ` +
          `Retrying in ${(totalWaitMs / 1000).toFixed(1)}s ` +
          `(attempt ${attempt + 1}/${MAX_RATE_LIMIT_RETRIES})`
        );
        await sleep(totalWaitMs);
        continue;
      }

      return response;
    } catch (error) {
      lastError = error;
      if (attempt >= MAX_RATE_LIMIT_RETRIES) break;

      const backoffMs = Math.min(1000 * (2 ** attempt), 10000);
      if (DEBUG) {
        console.warn(
          `Retrying ${label} (${attempt + 1}/${MAX_RATE_LIMIT_RETRIES}) ` +
          `after error: ${error.message}`
        );
      }
      await sleep(backoffMs);
    }
  }

  throw lastError;
}

function toDateTime(value, fallback) {
  if (!value) return fallback;
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? fallback : parsed.toISOString();
}

function logProgress(message) {
  const elapsedSeconds = ((Date.now() - START_TIME) / 1000).toFixed(1);
  console.log(`[+${elapsedSeconds}s] ${message}`);
}

function sanitizeId(id) {
  // Vertex AI requires IDs to match [a-zA-Z0-9-_]*
  // Replace dots and slashes with hyphens
  return id.replace(/[^a-zA-Z0-9-_]/g, '-');
}

function makeDoc(id, data) {
  const sanitized = sanitizeId(id);
  return {
    id: sanitized,
    structData: {
      id: sanitized,
      ...data
    }
  };
}

const ID_PATTERN = /^[a-zA-Z0-9-_]*$/;

function isIsoDateTime(value) {
  return typeof value === 'string' && !Number.isNaN(Date.parse(value));
}

function normalizeLabel(label) {
  if (typeof label === 'string') return label;
  if (label && typeof label.name === 'string') return label.name;
  return '';
}

function extractReferences(content, repo, defaultBranch) {
  const text = String(content || '');
  const refs = [];
  const seen = new Set();

  function addRef(rawText, targetUrl) {
    if (!rawText || !targetUrl) return;
    const key = `${rawText}::${targetUrl}`;
    if (seen.has(key)) return;
    seen.add(key);
    refs.push({ raw_text: rawText, target_url: targetUrl });
  }

  const discussionPattern = /\bdiscussion\s+#(\d+)\b/gi;
  for (const match of text.matchAll(discussionPattern)) {
    addRef(`#${match[1]}`, `https://github.com/${ORG}/${repo}/discussions/${match[1]}`);
  }

  const issuePattern = /\bissues?\s+#(\d+)\b/gi;
  for (const match of text.matchAll(issuePattern)) {
    addRef(`#${match[1]}`, `https://github.com/${ORG}/${repo}/issues/${match[1]}`);
  }

  const prPattern = /\b(?:pr|pull\s*request)\s+#(\d+)\b/gi;
  for (const match of text.matchAll(prPattern)) {
    addRef(`#${match[1]}`, `https://github.com/${ORG}/${repo}/pull/${match[1]}`);
  }

  const blobPathPattern = /\b([\w.-]+\.(?:md|markdown|mdx))\b/gi;
  for (const match of text.matchAll(blobPathPattern)) {
    addRef(match[1], `https://github.com/${ORG}/${repo}/blob/${defaultBranch}/${match[1]}`);
  }

  return refs;
}

function validateDoc(doc) {
  const errors = [];
  const data = doc?.structData;

  if (typeof doc.id !== 'string' || doc.id.length === 0 || !ID_PATTERN.test(doc.id)) {
    errors.push('invalid id');
  }

  if (!data || typeof data !== 'object' || Array.isArray(data)) {
    errors.push('missing structData');
    return { valid: false, errors };
  }

  if (typeof data.id !== 'string' || data.id !== doc.id) {
    errors.push('invalid structData.id');
  }
  if (typeof data.title !== 'string') errors.push('invalid title');
  if (typeof data.content !== 'string') errors.push('invalid content');
  if (typeof data.url !== 'string') errors.push('invalid url');
  if (typeof data.type !== 'string') errors.push('invalid type');
  if (typeof data.repo !== 'string') errors.push('invalid repo');
  if (typeof data.state !== 'string') errors.push('invalid state');
  if (typeof data.author !== 'string') errors.push('invalid author');
  if (!Array.isArray(data.labels) || data.labels.some(label => typeof label !== 'string')) {
    errors.push('invalid labels');
  }
  if (!isIsoDateTime(data.created_at)) errors.push('invalid created_at');
  if (!isIsoDateTime(data.updated_at)) errors.push('invalid updated_at');
  if (!Array.isArray(data.references)) {
    errors.push('invalid references');
  } else {
    for (const ref of data.references) {
      if (!ref || typeof ref !== 'object') {
        errors.push('invalid reference object');
        break;
      }
      if (typeof ref.raw_text !== 'string') errors.push('invalid reference raw_text');
      if (typeof ref.target_url !== 'string') errors.push('invalid reference target_url');
    }
  }
  if (data.number !== undefined && !Number.isInteger(data.number)) {
    errors.push('invalid number');
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

// Repos to index — add/remove as needed
const REPOS = [
  'medley',
  'Interlisp.github.io',
  'online',
  'maiko',
  'loops',
  'notecards',
  // add others here
];

async function githubFetch(url) {
  const resp = await githubRequest(url, { headers }, url);
  if (!resp.ok) {
    const body = await resp.text();
    const error = new Error(`GitHub API error ${resp.status}: ${url} :: ${body.slice(0, 300)}`);
    error.status = resp.status;
    error.url = url;
    throw error;
  }
  return resp.json();
}

function isNotFoundError(error) {
  return error && Number(error.status) === 404;
}

async function getDefaultBranch(repo) {
  const meta = await githubFetch(`https://api.github.com/repos/${ORG}/${repo}`);
  return {
    defaultBranch: meta.default_branch || 'main',
    repoUpdatedAt: toDateTime(meta.updated_at, new Date().toISOString())
  };
}

async function indexMarkdownFiles(repo, defaultBranch, repoUpdatedAt) {
  const docs = [];
  const treeResp = await githubFetch(
    `https://api.github.com/repos/${ORG}/${repo}/git/trees/${defaultBranch}?recursive=1`
  );
  const tree = treeResp.tree || [];
  const markdownFiles = tree.filter(entry =>
    entry.type === 'blob' &&
    /\.(md|markdown|mdx)$/i.test(entry.path) &&
    !/^README(\.[^/]+)?$/i.test(path.basename(entry.path))
  );

  for (const file of markdownFiles) {
    try {
      const blob = await githubFetch(
        `https://api.github.com/repos/${ORG}/${repo}/git/blobs/${file.sha}`
      );
      const content = Buffer.from(blob.content || '', 'base64').toString('utf-8');
      const trimmed = content.slice(0, 10000);
      const url = `https://github.com/${ORG}/${repo}/blob/${defaultBranch}/${file.path}`;
      docs.push(makeDoc(
        `gh-markdown-${repo}-${file.path.replace(/\//g, '-')}`,
        {
          title: `[${repo}] ${file.path}`,
          content: trimmed,
          url,
          references: extractReferences(trimmed, repo, defaultBranch),
          type: 'markdown',
          labels: [],
          repo,
          state: 'active',
          author: '',
          created_at: repoUpdatedAt,
          updated_at: repoUpdatedAt
        }
      ));
    } catch (e) {
      if (DEBUG) {
        console.warn(`Could not index markdown file ${repo}:${file.path}: ${e.message}`);
      }
    }
  }

  return docs;
}

async function* paginate(url, label = url) {
  let nextUrl = url;
  let page = 0;
  while (nextUrl) {
    page += 1;
    if (Number.isInteger(MAX_PAGES_PER_PAGINATION) && MAX_PAGES_PER_PAGINATION > 0 && page > MAX_PAGES_PER_PAGINATION) {
      console.warn(`Pagination capped for ${label} at ${MAX_PAGES_PER_PAGINATION} pages`);
      break;
    }
    if (DEBUG) {
      logProgress(`Fetching ${label} page ${page}`);
    }
    let resp;
    try {
      resp = await githubRequest(nextUrl, { headers }, `${label} page ${page}`);
    } catch (error) {
      console.warn(`Pagination stopped for ${label} at page ${page}: ${error.message}`);
      break;
    }
    if (!resp.ok) {
      const body = await resp.text();
      console.warn(`Pagination stopped for ${label} at page ${page}: HTTP ${resp.status} ${body.slice(0, 200)}`);
      break;
    }
    const data = await resp.json();
    yield* data;

    // Parse Link header for next page
    const link = resp.headers.get('Link') || '';
    const match = link.match(/<([^>]+)>;\s*rel="next"/);
    nextUrl = match ? match[1] : null;
  }
}

function truncateByChars(parts, maxChars) {
  const output = [];
  let used = 0;

  for (const part of parts) {
    if (!part) continue;
    const chunk = String(part).trim();
    if (!chunk) continue;
    if (used >= maxChars) break;

    const remaining = maxChars - used;
    if (chunk.length <= remaining) {
      output.push(chunk);
      used += chunk.length;
      continue;
    }

    output.push(chunk.slice(0, remaining));
    used = maxChars;
    break;
  }

  return output.join('\n\n');
}

function promiseWithTimeout(promise, timeoutMs, message) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(message)), timeoutMs);
    promise
      .then(value => {
        clearTimeout(timer);
        resolve(value);
      })
      .catch(error => {
        clearTimeout(timer);
        reject(error);
      });
  });
}

async function fetchPullRequestSearchSignals(repo, prNumber) {
  const changedFiles = [];
  const commitMessages = [];

  for await (const file of paginate(
    `https://api.github.com/repos/${ORG}/${repo}/pulls/${prNumber}/files?per_page=100`
  )) {
    if (typeof file.filename === 'string' && file.filename.length > 0) {
      changedFiles.push(file.filename);
    }
  }

  for await (const commit of paginate(
    `https://api.github.com/repos/${ORG}/${repo}/pulls/${prNumber}/commits?per_page=100`
  )) {
    const msg = commit.commit?.message;
    if (typeof msg === 'string' && msg.length > 0) {
      commitMessages.push(msg);
    }
  }

  return {
    changedFiles,
    commitMessages
  };
}

async function indexRepo(repo) {
  const docs = [];
  logProgress(`Indexing ${ORG}/${repo}...`);
  const { defaultBranch, repoUpdatedAt } = await getDefaultBranch(repo);

  logProgress(`${ORG}/${repo}: default branch is ${defaultBranch}`);

  // Index README
  try {
    logProgress(`${ORG}/${repo}: fetching README`);
    const readme = await githubFetch(
      `https://api.github.com/repos/${ORG}/${repo}/readme`
    );
    const content = Buffer.from(readme.content, 'base64').toString('utf-8');
    const trimmed = content.slice(0, 10000);
    const url = `https://github.com/${ORG}/${repo}/blob/${defaultBranch}/${readme.path || 'README.md'}`;
    docs.push(makeDoc(
      `gh-markdown-${repo}-readme`,
      {
        title: `${repo} README`,
        content: trimmed,
        url,
        references: extractReferences(trimmed, repo, defaultBranch),
        type: 'markdown',
        labels: [],
        repo,
        state: 'active',
        author: '',
        created_at: repoUpdatedAt,
        updated_at: repoUpdatedAt
      }
    ));
  } catch (e) {
    if (isNotFoundError(e)) {
      console.warn(`No README for ${repo}`);
    } else {
      console.warn(`README lookup failed for ${repo}: ${e.message}`);
    }
  }

  // Index all markdown files in the repository (excluding README files).
  try {
    logProgress(`${ORG}/${repo}: indexing markdown files`);
    const markdownDocs = await indexMarkdownFiles(repo, defaultBranch, repoUpdatedAt);
    docs.push(...markdownDocs);
    logProgress(`${ORG}/${repo}: indexed ${markdownDocs.length} markdown files`);
  } catch (e) {
    console.warn(`Could not index markdown files for ${repo}: ${e.message}`);
  }

  // Index Issues
  let issueCount = 0;
  for await (const issue of paginate(
    `https://api.github.com/repos/${ORG}/${repo}/issues?state=all&per_page=100`,
    `${ORG}/${repo} issues`
  )) {
    if (issue.pull_request) continue; // skip PRs here, handle separately
    issueCount += 1;
    const content = (issue.body || '').slice(0, 10000);
    docs.push(makeDoc(
      `gh-issue-${repo}-${issue.number}`,
      {
        title: issue.title,
        content,
        url: issue.html_url,
        references: extractReferences(content, repo, defaultBranch),
        type: 'issue',
        labels: (issue.labels || []).map(normalizeLabel).filter(Boolean),
        repo,
        state: issue.state,
        author: issue.user?.login || '',
        created_at: toDateTime(issue.created_at, repoUpdatedAt),
        updated_at: toDateTime(issue.updated_at, repoUpdatedAt),
        number: issue.number
      }
    ));

    if (issueCount === 1 || issueCount % 25 === 0) {
      logProgress(`${ORG}/${repo}: indexed ${issueCount} issues`);
    }
  }

  logProgress(`${ORG}/${repo}: finished issues (${issueCount})`);

  // Index Pull Requests
  let prCount = 0;
  for await (const pr of paginate(
    `https://api.github.com/repos/${ORG}/${repo}/pulls?state=all&per_page=100`,
    `${ORG}/${repo} pull requests`
  )) {
    prCount += 1;
    if (prCount === 1 || prCount % 10 === 0) {
      logProgress(`${ORG}/${repo}: processing PR ${prCount} (#${pr.number})`);
    }

    let prSignals = { changedFiles: [], commitMessages: [] };

    try {
      prSignals = await promiseWithTimeout(
        fetchPullRequestSearchSignals(repo, pr.number),
        20000,
        `Timed out fetching PR details for ${repo}#${pr.number}`
      );
    } catch (e) {
      if (DEBUG) {
        console.warn(`Could not fetch PR details ${repo}#${pr.number}: ${e.message}`);
      }
    }

    const content = truncateByChars([
      pr.body || '',
      prSignals.changedFiles.length > 0
        ? `Changed files:\n${prSignals.changedFiles.join('\n')}`
        : '',
      prSignals.commitMessages.length > 0
        ? `Commit messages:\n${prSignals.commitMessages.join('\n---\n')}`
        : ''
    ], 10000);

    docs.push(makeDoc(
      `gh-pr-${repo}-${pr.number}`,
      {
        title: pr.title,
        content,
        url: pr.html_url,
        references: extractReferences(content, repo, defaultBranch),
        type: 'pull_request',
        labels: (pr.labels || []).map(normalizeLabel).filter(Boolean),
        repo,
        state: pr.state,
        author: pr.user?.login || '',
        created_at: toDateTime(pr.created_at, repoUpdatedAt),
        updated_at: toDateTime(pr.updated_at, repoUpdatedAt),
        number: pr.number
      }
    ));
  }

  logProgress(`${ORG}/${repo}: finished pull requests (${prCount})`);

  // Index Discussions (requires GraphQL API)
  try {
    logProgress(`${ORG}/${repo}: fetching discussions`);
    const discussionsResp = await githubRequest('https://api.github.com/graphql', {
      method:  'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: `
        query {
          repository(owner: "${ORG}", name: "${repo}") {
            discussions(first: 100) {
              nodes {
                number
                title
                body
                url
                createdAt
                updatedAt
                author { login }
                category { name }
              }
            }
          }
        }
      `})
    });

    const discussionsData = await discussionsResp.json();
    const discussions = discussionsData.data?.repository?.discussions?.nodes || [];
    logProgress(`${ORG}/${repo}: found ${discussions.length} discussions`);

    discussions.forEach(d => {
      const content = (d.body || '').slice(0, 10000);
      docs.push(makeDoc(
        `gh-discussion-${repo}-${d.number}`,
        {
          title: d.title,
          content,
          url: d.url,
          references: extractReferences(content, repo, defaultBranch),
          type: 'discussion',
          labels: d.category?.name ? [d.category.name] : [],
          repo,
          state: 'open',
          author: d.author?.login || '',
          created_at: toDateTime(d.createdAt, repoUpdatedAt),
          updated_at: toDateTime(d.updatedAt, repoUpdatedAt),
          number: d.number
        }
      ));
    });
  } catch (e) {
    console.warn(`Could not fetch discussions for ${repo}:`, e.message);
  }

  return docs;
}

async function main() {
  const allDocs = [];

  for (const repo of REPOS) {
    try {
      logProgress(`Starting repo ${ORG}/${repo}`);
      const docs = await indexRepo(repo);
      allDocs.push(...docs);
      logProgress(`${ORG}/${repo}: produced ${docs.length} documents`);
    } catch (e) {
      console.error(`Failed to index ${repo}:`, e.message);
    }
  }

  const validDocs = [];
  let invalidCount = 0;

  for (const doc of allDocs) {
    const result = validateDoc(doc);
    if (result.valid) {
      validDocs.push(doc);
      continue;
    }

    invalidCount += 1;
    console.warn(
      `Skipping invalid document ${doc.id || '<missing-id>'}: ${result.errors.join(', ')}`
    );
  }

  const jsonl = validDocs.map(d => JSON.stringify(d)).join('\n');
  fs.writeFileSync(OUTPUT_FILE, jsonl);
  logProgress(`Wrote ${validDocs.length} valid documents to ${OUTPUT_FILE}`);
  if (invalidCount > 0) {
    console.warn(`Skipped ${invalidCount} invalid documents during pre-write validation`);
  }
}

//main().catch(console.error);
main();
