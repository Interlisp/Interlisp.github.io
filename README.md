# Interlisp.org Home Page

The documentation repository for <https://interlisp.org>, the restoration
project for the Interlisp ecosystem.

The collection of pages provides information on the restoration effort, Medley,
Interlisp and how to access and use the restored Medley system.

## Maintaining the website

The website is build using the [Hugo](https://gohugo.io/) static
site generator and the [Docsy](https://www.docsy.dev/) technical documentation
theme. Both of these sites contain a wealth of information on how to setup and
maintain a Hugo based website.

The process can be summarized as follows:

1. Clone the [Interlisp.github.io](https://github.com/Interlisp/Interlisp.github.io) repository
2. Edit or Add new pages
3. Validate the changes running Hugo locally
4. Add, Commit and Push the updates back to the Interlisp.github.io repository
5. Once the changes are merged into the `main` branch, `github actions` will rebuild and update the website

### Editing Existing Pages

Content is located in the `content/en` directory.  At present, English is the only language
supported by the web site.  If in the future, that changes, a new subdirectory can easily
be added to the `content` directory`.

Existing pages are written using [Markdown](https://www.markdownguide.org/tools/hugo/) and
can easily be edited.  Updates to pages can be submitted as a pull request and upon approval
will be merged in to the `main` branch to be deployed to the website.

### Adding New Pages

Each page must have a preamble section that provides metadata for the `Hugo` engine.  The format
is as follows:

```markdown
---
title: Medley Goals
weight: 10
type: docs
---
```

- Title: The displayed title for the page.
- Weight:  Specifies the positioning of the page.  Lower number pages are higher in the page order.  `Hugo` allows for multiple pages to be assigned the same weight.  
- Type: Identifies the type of the page.  Currently all pages are of type `docs`

The content to display on the page follows the preamble.  Content is written using [Markdown](https://www.markdownguide.org/tools/hugo/).  

Once authored the updated page can be submitted as a pull request and upon approval will be integrated
into the `main` branch and deployed to the website.

#### Adding or Updating the comments page

We've moved from 'Twitter' to a more general 'What people are saying' with quotes from social media.

For Twitter, the *comments* page uses images of Tweets of interest.  While `Hugo` has implemented a shortcode that will load the actual tweet, it
fails when the tweet no longer exists.  We believe there is value in keeping a record of conversations about Medley Interlisp and
to protect against losing portions of it, we have developed the practice of capturing an image of the tweet, using that on our page
and linking to the actual tweet.  

Tweets that are no longer accessible will have their links removed but the content will be preserved.  

The structure for new twitter entries on the *comments* page, the `_index.md` file in the `comments` directory is

```markdown
{{< imgproc PaulFord_20211214 Resize "550x803">}} <a href="https://twitter.com/ftrain/status/1470968024756895744?ref_src=twsrc">Link to tweet</a> {{< /imgproc >}}
```

We use the `imgproc` shortcode to render the image and size it.  The label for the image is a bit of html to link to the original tweet.  Lastly, the images
are titled with the author and the date of the tweet.  Ideally this will allow for easy identification of `jpeg` files.  The files are stored in the same
directory as the `_index.md` file, so everything needed for the page is packaged together.

### Bibliography.json

The web page maintains an extensive bibliography.  The information displayed on
the webpage is a snapshot of the data stored in our online [Zotero Group Library](https://www.zotero.org/groups/2914042/interlisp).

The webpage data is updated daily to help ensure it is an accurate
reflection of the bibliographic material related to Medley and Interlisp.

### gh-pages GitHub Workflow

Building the website is driven by a GitHub workflow.  

The workflow is triggered by one of two events, a `push` to main, representing updates
to the Interlisp.org website or a scheduled execution of the workflow.  The
workflow is scheduled to run on a regular basis to ensure the bibliography remains
consistent with the online Zotero catalog.

The GitHub Action workflow can also be initiated from the Action panel within
the Interlisp.github.io repository.  This option allows manual execution when
necessary.

The workflow consists of three jobs.  The first job, `check`, uses Zotero's REST
interface to query for the latest version of the group bibliography.  A `GET` call
is made to `https://api.zotero.org/groups/2914042/items`.  It
returns a collection of metadata and information describing the current state of
items within the catalog.  We are interested in a specific header, `Last-Modified-Version`.
The value returned with this header is incremented every time the Zotero Interlisp
catalog is updated.  We use the value returned as a cache-key for the bibliography.
If the cache-key matches one in the current GitHub Action cache we use the saved
bibliography information and save the overhead of building it.

The second job, `build`, starts by determining if a build and deploy need to occur.
If the workflow was initiated by a `push` a deploy will always be done.  However,
if the workflow was started by a scheduled execution and the Zotero bibliography
cache is consistent with the online Zotero catalog, the build and deploy are skipped.

A build starts by checking out the `Interlisp.github.io` repository.  Then,
if the Zotereo cache is valid, its contents are copied into the `data` file within the
repository directory structure.  If the cache is invalid, the `update_bibliography.sh`
shell script runs and downloads a new copy of the bibliography as a `json` file.
Once downloaded the script does some additional processing to complete the
formatting of the file.

After this work is completed, Hugo is setup and run to build the website. We use
Hugo extended to build our site. The version of Hugo currently being used is
defined by the environment variable, `HUGO_VERSION`.

We run Hugo with two flags:

- `-e $HUGO_ENVIRONMENT` to specify whether we are building a production or staging site.  If the website is being build to deploy to Interlisp.org,it should be built with `HUGO_ENVIRONMENT` set to production.  Deployment to any other site should set the environment flag to staging.
- `--cleanDestinationDir` clears the destination directory, `./public` on each build.  This will ensure we do not have any unneeded artifacts in our deployment.

The last part of the build activity is to save the created artifact, the information
in the `./public` directory.  We use the GitHub composition action `upload-pages-artifact`
for this.  It packages the contents of the directory and stores it in the appropriate
format for deployment to GitHub pages.

The last job in the tool chain is `deploy`.  This job simply takes the output
of the build step and formally deploys it to GitHub pages using the GitHub `deploy-pages`
action.

### Deploying a Staging Site

Successfully deploying a Staging Site requires you to configure your GitHub
repository to enable GitHub Pages.  The following steps will accomplish this task:

1. Clone the Interlisp.github.io repository into your GitHub site
2. In GitHub go to the cloned repository, in my case https://github.com/stumbo/InterlispDraft.github.io and select Settings
3. Under Settings, find Pages and select it
4. Under **Build and deployment** set Source to Deploy *GitHub Actions*

Once the repository is cloned and GitHub Pages has been setup, you can deploy a
staging site to validate changes prior to creating a Pull Request to merge your
changes back into the main site.

When creating a staging site we want to do a couple things to ensure we do not
interfere with the production site, first we want to disable Google Analytics
and secondly we want to ensure the site is not crawled and indexed.

#### Setup Your Repository

A best practice for the updating your clone of the repository is to create a branch
and make the following required changes on the branch you created.

The appropriate settings for this are all enabled by setting the `HUGO_ENVIRONMENT`
variable in `.github/workflows/gh-pages.yaml` to *staging*.

You also need to set `baseURL` to match the GitHub site you are deploying to
in the `config/staging/hugo.yaml` file.  The file currently looks like:

```yaml
baseURL: https://stumbo.github.io/InterlispDraft.github.io/

languageCode: en-us

# title
#  Insert Staging Environment onto every page to make clear
#  this is not the production site
title: 'Staging Environment'
```

Make sure the `baseURL` reflects the complete path of your repository.  Failure
to do this will either cause the deployment to fail or URLs within your built
site may be incorrectly set.  Resulting in 404s or expected resources not found.

With these changes the cloned repository is ready to be deployed to a staging site.

Commit the changes you made and push the new branch to your cloned repository.
At this point, create a Pull Request to merge the changes you made into your
repository's main branch.  Complete the operation by merging the pull request.

Once the merge occurs, the GitHub Actions should fire off and your site will be
built and deployed.

Once you have successfully completed this operation and your staging site is
deployed and operational you can experiment with adding new content or
functionality to the Interlisp site.

#### Develop a Feature

To develop new pages or functionality, create a new branch for your work.  once
you have completed development and testing on your staging site, you can create
a PR to merge the content into the Interlisp site.

### Running Hugo and Docsy Locally

Local testing of updates to the Interlisp.org website requires running `Hugo` locally.

To do this `Hugo` needs to be installed. Instructions for installing `Hugo` on a variety of operating systems can be
found at:  [Installing Hugo](https://gohugo.io/getting-started/installing).  Interlisp uses the extended version of Hugo.

For Ubuntu the following command works:

```bash
curl -s https://api.github.com/repos/gohugoio/hugo/releases/latest \
 | grep  browser_download_url \
 | grep linux-amd64.deb \
 | grep extended \
 | cut -d '"' -f 4 \
 | wget -i -

 sudo dpkg -i hugo_extended*linux-amd64.deb
```

The command can be adjusted for different architectures.

You can verify that `Hugo` is installed and working by running the following command:

```bash
hugo version
```

The response will be something along the lines of:

```bash
hugo v0.126.1-3d40aba512931031921463dafc172c0d124437b8+extended linux/amd64 BuildDate=2024-05-15T10:42:34Z VendorInfo=gohugoio
```

Be sure your version is at least `v0.122.0`. Older versions of `hugo` may fail to load correctly.

Secondly, there is one data file that is required to successfully build and run the `Interlisp.org` website locally, `static/data/bibliography.json`.
The production version of the website uses a GitHub Action to retrieve this file.
We can mimic that functionality by going to the `scripts` directory in your clone of the `Intelisp.github.io` repository.
Once in the directory, run the following command:

```bash
./update_bibliography.sh
```

This script will retrieve the bibliography from our Zotero library, format it appropriately and place the created file
in the appropriate location, the `static/data` directory.

This completes all the setup required for `Hugo`.

To run `Hugo` go to the root directory of your repository clone and run the following command:

```bash
hugo server --logLevel debug -v --renderToMemory -e development
```

`Hugo` will start and automatically download the Docsy theme and its dependencies as hugo modules.  You should see output along the lines of:

```bash
Watching for changes in /home/wstumbo/development/stumbo.github.io/{archetypes,content,layouts,package.json,static}
Watching for config changes in /home/wstumbo/development/stumbo.github.io/config/_default, /home/wstumbo/development/stumbo.github.io/config/development, /home/wstumbo/development/stumbo.github.io/go.mod
Start building sites …
hugo v0.126.1-3d40aba512931031921463dafc172c0d124437b8+extended linux/amd64 BuildDate=2024-05-15T10:42:34Z VendorInfo=gohugoio


                   | EN
-------------------+-----
  Pages            | 52
  Paginator pages  |  0
  Non-page files   | 46
  Static files     | 97
  Processed images | 47
  Aliases          | 66
  Cleaned          |  0

Built in 3230 ms
Environment: "development"
Serving pages from memory
Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
Web Server is available at //localhost:1313/ (bind address 127.0.0.1)
Press Ctrl+C to stop
```

`Hugo` is now running.  You can go to [http://localhost:1313](http://localhost:1313) to review the locally running version of the website.  
For most changes you should be able to review the text and layout to validate the effects are as expected.

You can get additional debugging information by adding the following two options
to your `hugo` command `--logLevel debug -v`.  

Once you have validated your changes, create a pull request to merge your changes into the `main` branch.

## Layout of the `Interlisp.github.io` repository

The layout of the `Interlisp.github.io` repository follows the standard [`Hugo` directory structure](https://gohugo.io/getting-started/directory-structure/).  Directories
that have components specific to `Interlisp.github.io` are as follows:

- `.github\workflows`  - home to the github actions `gh-pages.yml` that specifies how to build and release the Interlisp home page
- `assets` - customization of the `Docsy` theme for Interlisp.
  - `icons` - holds and `svg` version of `Interlisp-D' logo.  This logo is used in the page header
  - `scss` - contains some custom `scss`
    - `_styles_project.scss` sets the size of the `svg` file in the header and disables the edit page functionality
    - `main.scss` - links in the `scss` updates
- `config` - contains all the site specific configuration information
  - `_default` - configuration information shared across different supported environments [development, staging, production]
  - `development` - configuration information specific to the development environment
  - `production` - configuration information specific to the production environment
  - `staging` - configuration information specific to the staging environment
- `content\en` - home of all the content for the web page.  We currently only support the English language.  `Hugo` supports multiple languages and we have not disabled that feature. However there are no plans at present to transcribe the web pages and documentation into another language.
- `layout`
  - `shortcodes` - a simple snippet inside a content file that Hugo will render using a predefined template
    - `bibTable.html` - a shortcode used to format the [bibliography table](https://interlisp.org/bibliography/)
- `static` - the data in this folder is copied directly into the folder structure of the home page 
  - `css` - custom css files 
  - `data`  - holds `bibliography.json` used to create the [bibliography table](https://interlisp.org/bibliography/)
  - `documentation` - contains the pdf files referenced in the document section of the home page
  - `favicons` - contains `favicon.png` a small icon that browsers can use when referencing the website
  - `Resources` - contains the current `Interlisp-D` logo, used on the home page, and another instance of `favicon.png`
  - `CNAME` - a one line text file that provides support for using a [custom domain](https://gohugo.io/hosting-and-deployment/hosting-on-github/#use-a-custom-domain)

## Search

`Interlisp.org` uses Google Custom Search to provide search results encompassing
the `Interlisp.org` website, our GitHub sites used for continued development of
Medley Interlisp, and the discussions groups associated with both the Medley project and
Interlisp.

The search engine is identified in the `config/params.yaml` file:

```yaml
# Google custom seach engine configuration
#  gcs_engine_id:  search engine 
gcs_engine_id: 33ef4cbe0703b4f3ax
```

Search results are returned and presented using the page template, `search.md`.
The page template currently contains only a `yaml` header specifying the
layout as being `search`.

### Updating Search

Modifying the websites that are searched requires updating the Google Custom
Search engine settings.  This is done via logging into Google's Programmable Search
Engine Dashboard at:  [https://programmablesearchengine.google.com](https://programmablesearchengine.google.com)

Access to the Programmable Search Engine Dashboard is restricted.  To suggest updates or changes
open an issue:  [Search Engine Issue](https://github.com/interlisp/medley/issues/new?template=bug_report.md&title=Search_Engine_Issue)
