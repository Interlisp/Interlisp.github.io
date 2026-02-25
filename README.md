# Interlisp.org Home Page

[![GitHub Pages Deploy](https://github.com/Interlisp/Interlisp.github.io/actions/workflows/gh-pages.yml/badge.svg)](https://github.com/Interlisp/Interlisp.github.io/actions/workflows/gh-pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Hugo](https://img.shields.io/badge/Hugo-0.155.3-ff4088?logo=hugo)](https://gohugo.io/)
[![Docsy](https://img.shields.io/badge/Theme-Docsy-blue)](https://www.docsy.dev/)

The documentation repository for <https://interlisp.org>, the restoration
project for the Interlisp ecosystem.

The collection of pages provides information on the restoration effort, Medley,
Interlisp and how to access and use the restored Medley system.

## Table of Contents

- [Getting Started](#getting-started)
  - [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
- [Content Authoring](#content-authoring)
  - [Editing Existing Pages](#editing-existing-pages)
  - [Adding New Pages](#adding-new-pages)
  - [Adding or Updating the Comments Page](#adding-or-updating-the-comments-page)
  - [Bibliography Data](#bibliography-data)
- [Local Development](#local-development)
  - [Installing Hugo](#installing-hugo)
  - [Running the Development Server](#running-the-development-server)
- [CI/CD and Deployment](#cicd-and-deployment)
  - [gh-pages GitHub Workflow](#gh-pages-github-workflow)
  - [Environment Variables](#environment-variables)
  - [Deploying a Staging Site](#deploying-a-staging-site)
- [Reference](#reference)
  - [Repository Layout](#repository-layout)
  - [Dependencies](#dependencies)
  - [Search Configuration](#search-configuration)
- [Contact and Support](#contact-and-support)
- [License](#license)

---

## Getting Started

The website is built using the [Hugo](https://gohugo.io/) static site generator and the [Docsy](https://www.docsy.dev/) technical documentation theme. Both sites contain extensive documentation on setup and maintenance.

### Quick Start

For experienced users who want to get started quickly:

```bash
# Clone the repository
git clone https://github.com/Interlisp/Interlisp.github.io.git
cd Interlisp.github.io

# Fetch bibliography data (required for build)
./scripts/update_bibliography.sh

# Start local development server
hugo server -e development
```

Then open <http://localhost:1313> in your browser.

### Prerequisites

Before working with this repository, ensure you have the following installed:

| Tool | Version | Purpose |
|------|---------|--------|
| [Hugo Extended](https://gohugo.io/installation/) | v0.145.0+ | Static site generator |
| [Go](https://go.dev/doc/install) | 1.24+ | Required for Hugo modules |
| [Node.js & npm](https://nodejs.org/) | Latest LTS | PostCSS and autoprefixer |
| [jq](https://jqlang.github.io/jq/) | Latest | Bibliography JSON processing |
| curl, wget | System default | Script downloads |

**Verify installations:**

```bash
hugo version      # Should show "extended" and v0.145.0+
go version        # Should show 1.24+
node --version    # Should show v18+ or later
jq --version      # Any recent version
```

---

## Content Authoring

This section covers how to add and edit content on the Interlisp.org website.

**General workflow:**

1. Clone the [Interlisp.github.io](https://github.com/Interlisp/Interlisp.github.io) repository
2. Edit or add new pages
3. Validate the changes by running Hugo locally
4. Add, commit and push the updates back to the repository
5. Once merged into `main`, GitHub Actions will rebuild and update the website

### Editing Existing Pages

Content is located in the `content/en` directory. At present, English is the only language supported. If that changes in the future, additional language subdirectories can be added to the `content` directory.

Existing pages are written using [Markdown](https://www.markdownguide.org/tools/hugo/) and can easily be edited. Updates can be submitted as a pull request and, upon approval, will be merged into the `main` branch and deployed to the website.

### Adding New Pages

Each page must have a preamble section that provides metadata for the Hugo engine:

```markdown
---
title: Medley Goals
weight: 10
type: docs
---
```

| Field | Description |
|-------|-------------|
| `title` | The displayed title for the page |
| `weight` | Positioning of the page (lower numbers appear first). Multiple pages can share the same weight. |
| `type` | Page type. Currently all pages are of type `docs` |

The content follows the preamble and is written using [Markdown](https://www.markdownguide.org/tools/hugo/).

### Adding or Updating the Comments Page

The *comments* page ("What people are saying") collects quotes and screenshots that discuss Medley Interlisp. We preserve Twitter and Mastodon posts as images along with links to the post to protect against content being deleted from social platforms.

To add a new entry to the comments page (`content/en/project/comments/_index.md`):

```markdown
{{< imgproc AuthorName_YYYYMMDD Resize "550x803">}} <a href="https://example.com/post-url">Link to post</a> {{< /imgproc >}}
```

- Use the `imgproc` shortcode to render and size the image
- Name images with the author and date (e.g., `PaulFord_20211214.jpg`)
- Store image files in the same directory as `_index.md`
- Posts that are no longer accessible will have their links removed but the content will be preserved

### Bibliography Data

The website maintains an extensive bibliography. The information displayed on the webpage is a snapshot of the data stored in our online [Zotero Group Library](https://www.zotero.org/groups/2914042/interlisp). The Zotero library is our source of truth.

A GitHub Action runs daily to check if the Zotero library has changed. If so, a [script](https://github.com/Interlisp/Interlisp.github.io/blob/main/scripts/update_bibliography.sh) downloads and rebuilds the bibliography pages.

To fetch the bibliography locally:

```bash
cd scripts
./update_bibliography.sh
```

This script retrieves the bibliography from Zotero, formats it appropriately, and places the individual JSON files in `static/data/bibItems/`.

---

## Local Development

Local testing of updates requires running Hugo locally.

### Installing Hugo

Instructions for installing Hugo on various operating systems are at: [Installing Hugo](https://gohugo.io/getting-started/installing). **Interlisp uses the extended version of Hugo.**

For Ubuntu:

```bash
curl -s https://api.github.com/repos/gohugoio/hugo/releases/latest \
 | grep  browser_download_url \
 | grep linux-amd64.deb \
 | grep extended \
 | cut -d '"' -f 4 \
 | wget -i -

sudo dpkg -i hugo_extended*linux-amd64.deb
```

Verify installation:

```bash
hugo version
# Expected output (version should be v0.145.0 or later):
# hugo v0.126.1-3d40aba512931031921463dafc172c0d124437b8+extended linux/amd64 ...
```

### Running the Development Server

1. Ensure bibliography data is available (see [Bibliography Data](#bibliography-data))

2. Start the Hugo development server:

```bash
 hugo server --cleanDestinationDir  --disableFastRender --renderToMemory
```

Hugo will automatically download the Docsy theme and its dependencies as Hugo modules. Expected output:

```bash
Watching for changes in /home/wstumbo/development/Interlisp.github.io/archetypes, /home/wstumbo/development/Interlisp.github.io/assets/{css,icons,js,scss}, /home/wstumbo/development/Interlisp.github.io/content/en/{history,project,software}, /home/wstumbo/development/Interlisp.github.io/layouts/{_default,_partials,_shortcodes,bibliography,redirect}, /home/wstumbo/development/Interlisp.github.io/package.json, /home/wstumbo/development/Interlisp.github.io/static/{Resources,data,docs,documentation,favicons}
Watching for config changes in /home/wstumbo/development/Interlisp.github.io/config/_default, /home/wstumbo/development/Interlisp.github.io/config/development, /home/wstumbo/development/Interlisp.github.io/go.mod
Start building sites … 
hugo v0.155.2-d8c0dfccf72ab43db2b2bca1483a61c8660021d9+extended+withdeploy linux/amd64 BuildDate=2026-02-02T10:04:51Z VendorInfo=gohugoio

WARN  WARNING: 298 sidebar entries have been truncated. To avoid this, increase `params.ui.sidebar_menu_truncate` to at least 398 (from 100) in your config file. Section: /history/bibliography

                  │  EN  
──────────────────┼──────
 Pages            │ 1165 
 Paginator pages  │    0 
 Non-page files   │   66 
 Static files     │   79 
 Processed images │   50 
 Aliases          │   51 
 Cleaned          │    0 

Built in 1169 ms
Environment: "development"
Serving pages from memory
Web Server is available at //localhost:1313/ (bind address 127.0.0.1) 
Press Ctrl+C to stop
```

3. Open <http://localhost:1313> to review the locally running website

4. For additional debugging information, use `--logLevel debug`

Once validated, create a pull request to merge your changes into the `main` branch.

---

## CI/CD and Deployment

This section covers automated builds and deployment processes.

### gh-pages GitHub Workflow

Building the website is driven by a GitHub workflow (`.github/workflows/gh-pages.yml`).

**Triggers:**

- `push` to main — updates to the Interlisp.org website
- Scheduled execution — ensures the bibliography remains consistent with Zotero
- Manual execution — via the Actions panel in GitHub

**Workflow Jobs:**

The workflow consists of three jobs:

**1. `check` — Verify Bibliography Currency**

Uses Zotero's REST interface to query for the latest version of the group bibliography. A `GET` call is made to:

```
https://api.zotero.org/groups/2914042/items
```

This returns metadata including the `Last-Modified-Version` header, which is incremented every time the Zotero Interlisp catalog is updated. This value is used as a cache key for the bibliography. If the cache key matches one in the current GitHub Action cache, we reuse the saved bibliography and skip rebuilding.

**2. `build` — Build the Website**

- Determines if a build is needed:
  - On `push`: Always builds and deploys
  - On schedule: Skips build if Zotero cache is current
- Checks out the repository
- If the Zotero cache is valid, copies its contents into the `data` directory
- If the cache is invalid, runs `update_bibliography.sh` to download and process a new copy
- Runs Hugo Extended (version defined by `HUGO_VERSION` environment variable) with flags:
  - `-e $HUGO_ENVIRONMENT` — specifies production or staging build
  - `--cleanDestinationDir` — clears `./public` directory to avoid stale artifacts
- Uses the GitHub `upload-pages-artifact` action to package and store the `./public` directory contents for deployment

**3. `deploy` — Deploy to GitHub Pages**

Takes the output of the build step and deploys it to GitHub Pages using the GitHub `deploy-pages` action.

### Environment Variables

The following environment variables control the build and deployment process:

| Variable | Description | Values | Default |
|----------|-------------|--------|---------|
| `HUGO_ENVIRONMENT` | Specifies the build environment | `development`, `staging`, `production` | `staging` |
| `HUGO_VERSION` | Hugo version used in CI/CD | Semantic version (e.g., `0.155.3`) | Set in workflow |

**Environment-specific behavior:**

| Environment | Analytics | Crawlers | Use Case |
|-------------|-----------|----------|----------|
| `production` | Enabled | Allowed | Live interlisp.org site |
| `staging` | Disabled | Blocked | PR previews and testing |
| `development` | Disabled | N/A | Local development |

These variables are set in `.github/workflows/gh-pages.yml` and can be overridden via GitHub repository variables.

### Deploying a Staging Site

To deploy a personal staging site for testing:

**1. Initial Setup:**

1. Fork/clone the Interlisp.github.io repository to your GitHub account
2. In your repository, go to **Settings → Pages**
3. Under **Build and deployment**, set Source to **Deploy from GitHub Actions**

**2. Configure Your Fork:**

Create a branch and make these required changes:

1. Set `HUGO_ENVIRONMENT` to `staging` in `.github/workflows/gh-pages.yaml`

2. Update `baseURL` in `config/staging/hugo.yaml` to match your repository:

```yaml
baseURL: https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/

languageCode: en-us
title: 'Staging Environment'
```

> **Important:** The `baseURL` must reflect the complete path of your repository. Incorrect URLs will cause deployment failures or broken links.

**3. Deploy:**

1. Commit and push your branch
2. Create a Pull Request to merge into your repository's main branch
3. Merge the PR — GitHub Actions will build and deploy your staging site

**4. Develop Features:**

Create feature branches for new work. Once tested on your staging site, create a PR to merge content into the main Interlisp repository.

---

## Reference

### Repository Layout

The repository follows the standard [Hugo directory structure](https://gohugo.io/getting-started/directory-structure/):

| Directory | Purpose |
|-----------|---------|
| `.github/workflows` | GitHub Actions workflow (`gh-pages.yml`) |
| `assets/` | Custom global resources (CSS, JS, icons, SCSS) |
| `config/` | Site configuration for different environments |
| `content/en/` | All website content (English only) |
| `layouts/` | Hugo layout templates and overrides |
| `static/` | Files copied directly to the built site |

**Key subdirectories:**

<details>
<summary><strong>assets/</strong> — Custom resources</summary>

- `css/` — Third-party CSS files
- `icons/` — SVG Interlisp-D logo (`logo.svg`)
- `js/` — Custom and third-party JavaScript
- `scss/` — Custom SCSS files
  - `_styles_project.scss` — Project-specific styles
  - `_variables_project.scss` — Docsy theme variable overrides

</details>

<details>
<summary><strong>config/</strong> — Environment configurations</summary>

- `_default/` — Shared settings across all environments
- `development/` — Local development settings
- `staging/` — Staging site settings
- `production/` — Production site settings

</details>

<details>
<summary><strong>layouts/</strong> — Template overrides</summary>

- `_partials/` — Partial templates (favicons, footer, head, meta descriptions)
- `_shortcodes/` — Hugo shortcodes (cover block, image gallery)
- `bibliography/` — Bibliography section templates
- `redirect/` — Redirect page template

</details>

<details>
<summary><strong>static/</strong> — Static files</summary>

- `data/bibItems/` — Bibliography JSON files (generated, not in Git)
- `documentation/` — PDF files referenced in the website
- `favicons/` — Favicon files (SVG, ICO, PNG)
- `Resources/` — Site resources including watermark logo
- `CNAME` — Custom domain configuration

</details>

### Dependencies

**Hugo Modules (go.mod):**

| Module | Version | Purpose |
|--------|---------|---------|
| [google/docsy](https://github.com/google/docsy) | v0.14.3 | Technical documentation theme |
| docsy/dependencies | v0.7.2 | Docsy's required dependencies |

Hugo modules are automatically downloaded when you run `hugo server` or `hugo build`.

**npm Packages (package.json):**

| Package | Purpose |
|---------|---------|
| autoprefixer | Adds vendor prefixes to CSS for browser compatibility |
| hugo-extended | Hugo binary for npm-based workflows |
| postcss / postcss-cli | CSS transformation pipeline |
| jquery | JavaScript library used by some Docsy components |
| tabpanel | Accessible tab panel widget |

Install npm dependencies with `npm install` (optional for local development).

### Search Configuration

The site uses Google Custom Search to provide search results encompassing:
- The Interlisp.org website
- Interlisp GitHub repositories
- Discussion groups for Medley and Interlisp

The search engine is configured in `config/params.yaml`:

```yaml
gcs_engine_id: 33ef4cbe0703b4f3ax
```

Search results are rendered using the `search.html` layout template.

**Updating Search:**

Modifying search scope requires updating the Google Custom Search engine settings via the [Programmable Search Engine Dashboard](https://programmablesearchengine.google.com). Access is restricted. To suggest changes, open an issue: [Search Engine Issue](https://github.com/interlisp/medley/issues/new?template=bug_report.md&title=Search_Engine_Issue)

---

## Contact and Support

- **Report Issues**: [GitHub Issues](https://github.com/Interlisp/Interlisp.github.io/issues) — Report bugs or request features for the website
- **Medley Interlisp Issues**: [Medley Repository](https://github.com/Interlisp/medley/issues) — For issues related to Medley itself
- **Discussions**: [Interlisp Discussions](https://github.com/orgs/Interlisp/discussions) — Community discussions and questions
- **Mailing List**: [interlisp@googlegroups.com](https://groups.google.com/g/interlisp) — General Interlisp community discussion

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Interlisp.org
