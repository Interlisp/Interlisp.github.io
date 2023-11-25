# Interlisp.org Home Page

The documentation repository for <https://interlisp.org>, the restoration
project for the Interlisp ecosystem. This is a revision by Andrew Sengul.

The collection of pages provides information on the restoration effort, Medley,
Interlisp and how to access and use the restored Medley system.

## Mainitaining the website

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

The workflow is trigger by one of two events, a `push` to main, representing updates
to the Interlisp.org website or a scheduled execution of the workflow.  The
workflow is scheduled to run on a regular basis to ensure the bibliography remains
consistent with the online Zotero catalog.

The workflow consists of two jobs.  The first job, `check`, uses Zotero's REST
interface to query for the latest version of the group bibliography.  The call
made is a `GET` call to `https://api.zotero.org/groups/2914042/items`.  This call
returns a collection of metadata and information describing the current state of
items within the catalog.  We are interested in a specific header, `Last-Modified-Version`.
The value returned with this header is incremented every time the Zotero Interlisp
catalog is updated.  The value returned is used as a cache-key for a cached
version of the json file of the bibliography we create.  The first job completes
by providing the current Zotero version and whether the cache needs to be updated.

The second job, `deploy`, starts by determining if a deploy needs to occur.  If
the workflow was initiated by a `push` a deploy will always be done.  However,
if the workflow was started by a scheduled execution, if the Zotero bibliography
cache is consistent with the online Zotero catalog, the deploy is skipped.

A deploy starts by checking out the `Interlisp.github.io` repository.  Then,
if the cache is valid, the contents are copied into the `data` file within the
repository directory structure.  If the cache is invalid, the `update_bibliography.sh`
shell script is run to download a new copy of the bibliography as a `json` file.
Once downloaded the script does some additional processing to complete the
formatting of the file.

Once this work is completed, Hugo is setup and the website is deployed.


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
hugo v0.111.3-5d4eb5154e1fed125ca8e9b5a0315c4180dab192+extended linux/amd64 BuildDate=2023-03-12T11:40:50Z VendorInfo=gohugoio
```

Be sure your version is at least `v0.101.0`. Older versions of `hugo` may fail to load correctly.

Secondly, there is one data file that is required to successfully build and run the `Interlisp.org` website locally, `data/bibliography.json`.
The production version of the website uses a GitHub Action to retrieve this file.
We can mimic that functionality by going to the `scripts` directory in your clone of the `Intelisp.github.io` repository.
Once in the directory, run the following command:

```bash
./update_bibliography.sh
```

This script will retrieve the bibliography from our Zotero library, format it appropriately and place the created file
in the appropriate location, the `data` directory.

This completes all the setup required for `Hugo`.

To run `Hugo` go to the root directory of your repository clone and run the following command:

```bash
hugo server
```

`Hugo` will start and automatically download the Docsy theme and it's dependencies as hugo modules.  You should see output along the lines of:

```bash
hugo: downloading modules …
hugo: collected modules in 17781 ms
Start building sites …
hugo v0.111.3-5d4eb5154e1fed125ca8e9b5a0315c4180dab192+extended linux/amd64 BuildDate=2023-03-12T11:40:50Z VendorInfo=gohugoio

                   | EN
-------------------+-----
  Pages            | 61
  Paginator pages  |  0
  Non-page files   | 13
  Static files     | 68
  Processed images | 46
  Aliases          |  4
  Sitemaps         |  1
  Cleaned          |  0

Built in 1349 ms
Watching for changes in /home/wstumbo/development/Interlisp.github.io/{archetypes,assets,content,data,layouts,package.json,static,themes}
Watching for config changes in /home/wstumbo/development/Interlisp.github.io/config.toml, /home/wstumbo/development/Interlisp.github.io/go.mod
Environment: "development"
Serving pages from memory
Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)
Press Ctrl+C to stop
```

`Hugo` is now running.  You can go to [http://localhost:1313](http://localhost:1313) to review the locally running version of the website.  
For most changes you should be able to review the text and layout to validate the effects are as expected.

Once you have validated your changes, create a pull request to merge your changes into the `main` branch.

## Layout of the `Interlisp.github.io` repository

The layout of the `Interlisp.github.io` repository follows the standard [`Hugo` directory structure](https://gohugo.io/getting-started/directory-structure/).  Directories
that have components specific to `Interlisp.github.io` are as follows:

- `.` - at the root, `config.toml` file provides the general site configuration information
- `.github\workflows`  - home to the github actions `gh-pages.yml` that specifies how to build and release the Interlisp home page
- `assets` - customization of the `Docsy` theme for Interlisp.
  - `icons` - holds and `svg` version of `Interlisp-D' logo.  This logo is used in the page header
  - `scss` - contains some custom `scss`
    - `_styles_project.scss` sets the size of the `svg` file in the header and disables the edit page functionality
    - `main.scss` - links in the `scss` updates
- `content\en` - home of all the content for the web page.  We currently only support the English language.  `Hugo` supports multiple languages and we have not disabled that feature. However there are no plans at present to transcribe the web pages and documentation into another language.
- `data`  - holds `bibliography.json` used to create the [bibliography table](https://interlisp.org/bibliography/)
- `layout`
  - `shortcodes` - a simple snippet inside a content file that Hugo will render using a predefined template
    - `bibTable.html` - a shortcode used to format the [bibliography table](https://interlisp.org/bibliography/)
- `static` - the data in this folder is copied directly into the folder structure of the home page  
  - `documentation` - contains the pdf files referenced in the document section of the home page
  - `favicons` - contains `favicon.png` a small icon that browsers can use when referencing the website
  - `Resources` - contains the current `Interlisp-D` logo, used on the home page, and another instance of `favicon.png`
  - `CNAME` - a oneline text file that provides support for using a [custom domain](https://gohugo.io/hosting-and-deployment/hosting-on-github/#use-a-custom-domain)

## Search

`Interlisp.org` uses Google Custom Search to provide search results encompassing
the `Interlisp.org` website, our GitHub sites used for continued development of
Medley Interlisp, and the discussions groups associated with both the Medley project and
Interlisp.

The search engine is identified in the `hugo.toml` file:

```toml
# Google Custom Search Engine ID. Remove or comment out to disable search.
gcs_engine_id = "33ef4cbe0703b4f3a"
```

Search results are returned and presented using the page template, `search.md`.
The page template currently contains only a `yaml` header specifying the
layout as being `search`.

### Updating Search

Modfying the websites that are searched requires updating the Google Custom
Search engine settings.  This is done via logging into Google's Programmable Search
Engine Dashboard at:  [https://programmablesearchengine.google.com](https://programmablesearchengine.google.com)

Access to the Programmable Search Engine Dashboard is restricted.  To suggest updates or changes
open an issue:  [Search Engine Issue](https://github.com/interlisp/medley/issues/new?template=bug_report.md&title=Search_Engine_Issue)
