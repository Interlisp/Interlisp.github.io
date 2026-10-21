---
title: "Zotero Type Mapping Reference"
description: "How Interlisp Zotero bibliography types map to CSL JSON and Schema.org vocabulary"
type: docs
toc_hide: false
---

## Purpose

This page documents how bibliography entry types are classified and mapped through the processing pipeline. It serves as a reference for:

- **Content creators** contributing to the Interlisp Zotero group who want to understand how their entries will be categorized
- **Developers** working on the bibliography processing system who need to know current type support
- **Data consumers** using the JSON-LD output who need to understand what schema.org types represent Interlisp bibliography entries

The mapping chain flows through three formats:

```
Zotero Item Type → CSL JSON Type → Schema.org @type
```

Each format serves a different purpose:

- **Zotero Item Type**: Classification used within Zotero (the source system)
- **CSL JSON Type**: Standardized format for citation metadata (intermediate processing format)
- **Schema.org @type**: Structured data markup for web search engines and semantic web consumers (output format)

A Zotero item type maps to exactly one CSL JSON type. The CSL JSON type is what the rest of the pipeline sees, and it is the value recorded as `item_type` in each bibliography entry's front matter.

---

## Type Reference Table

| Zotero Item Type | CSL Type | Schema.org @type | additionalType | genre | Status | Notes |
|---|---|---|---|---|---|---|
| **Journal Article** | `article-journal` | `ScholarlyArticle` | — | — | ✅ Implemented | Peer-reviewed journal articles, conference proceedings in journals |
| **Magazine Article** | `article-magazine` | `Article` | — | — | ✅ Implemented | Magazine and trade publication articles |
| **Newspaper Article** | `article` | `Article` | — | — | ✅ Implemented | Newspaper articles and news items |
| **Book** | `book` | `Book` | — | — | ✅ Implemented | Books and monographs |
| **Book Section** | `chapter` | `Chapter` | — | — | ✅ Implemented | Chapters or sections within books |
| **Conference Paper** | `paper-conference` | `ScholarlyArticle` | — | — | ✅ Implemented | Papers presented at conferences (when not in proceedings) |
| **Report** | `report` | `Report` | the entry's report type | — | ✅ Implemented | Technical reports, working papers, government documents |
| **Thesis** | `thesis` | `Thesis` | — | — | ✅ Implemented | Master's theses, dissertations, doctoral theses |
| **Patent** | `patent` | `CreativeWork` | `"Patent"` | — | ✅ Implemented | Patents and patent applications |
| **Blog Post** | `post-weblog` | `BlogPosting` | — | — | ✅ Implemented | Blog posts and web log entries |
| **Webpage** | `webpage` | `WebPage` | — | — | ✅ Implemented | General web pages and websites |
| **Encyclopedia Entry** | `entry-encyclopedia` | `Article` | — | — | ✅ Implemented | Encyclopedia and reference work entries |
| **Film** | `motion_picture` | `VideoObject` | — | — | ✅ Implemented | Films, videos, and visual media |
| **Email** | `personal_communication` | `Message` | — | — | ✅ Implemented | Personal communications, emails, letters |
| **Computer Program** | `software` | `SoftwareSourceCode` | — | — | 📋 Planned | Software, source code repositories, applications, tools. The Type field names the programming language. |
| **Document** | `document` | `CreativeWork` | `"TechnicalDocumentation"` | — | 📋 Planned | Technical manuals, guides, user documentation, software docs, specifications |
| **Document** with Type `Transcript` | `document` | `CreativeWork` | `"Transcript"` | `"Transcript"` | 📋 Planned | Oral history interviews, recorded interviews, media transcripts |
| **Standard** | `standard` | `CreativeWork` | `"Standard"` | — | 📋 Planned | Technical standards, specifications, protocols, standards documents. The Type field names the standard's series or designation. |

### Legend

- **✅ Implemented**: The type is fully supported. The processing pipeline emits it and the generated JSON-LD carries the Schema.org mapping shown.
- **📋 Planned**: The type is recognised and has a defined Schema.org mapping, but the processing pipeline does not yet emit it. Entries of this type are published without the Schema.org markup described above.
- **Zotero Item Type**: The classification used in Zotero's item type selector
- **CSL Type**: The type value in CSL JSON output from Zotero API
- **Schema.org @type**: The `@type` field in generated JSON-LD
- **additionalType**: Optional `additionalType` field in JSON-LD for additional classification
- **genre**: Optional `genre` field in JSON-LD for the entry's genre

---

## Type Categories and Use Cases

### Publishing Types (Peer-Reviewed and Published)

These types are for published, citable research and writing:

- **Journal Article** (`article-journal`): Peer-reviewed journal papers, conference proceedings published in journals
- **Magazine Article** (`article-magazine`): Trade magazines, popular science magazines
- **Newspaper Article** (`article`): Newspaper articles and news publications
- **Conference Paper** (`paper-conference`): Conference proceedings and papers
- **Book** (`book`): Published books and monographs
- **Book Section** (`chapter`): Chapters within books
- **Thesis** (`thesis`): Academic theses and dissertations

### Technical and Professional Types

- **Report** (`report`): Technical reports, working papers, government reports, internal documentation
- **Patent** (`patent`): Patents and patent applications
- **Encyclopedia Entry** (`entry-encyclopedia`): Reference works and encyclopedia entries
- **Standard** (`standard`): Technical standards, protocols, standardization documents

### Documentary Types

- **Document** (`document`): Broad category for technical documentation, user guides, specifications, manuals
  - The Zotero **Type** field distinguishes subcategories within this item type. For an oral-history interview — a written document recording a conversation between an interviewer and an interviewee — set the Type field to `Transcript`. Its schema.org mapping is `additionalType: "Transcript"` with `genre: "Transcript"`.
  - Other Type values are carried through to the Schema.org `genre` property. For example, a document with a Type of `Newsletter` maps to `genre: "Newsletter"`.
- **Standard** (`standard`): The Zotero **Type** field names the standard's series or designation (for example, `Xerox System Integration Standard`). Its schema.org mapping is `isPartOf` → `CreativeWorkSeries`.

### Digital and Media Types

- **Webpage** (`webpage`): Web pages, online resources, digital articles
- **Blog Post** (`post-weblog`): Blog entries and web logs
- **Film** (`motion_picture`): Videos, films, recorded presentations, documentaries
- **Computer Program** (`software`): Software repositories, source code, applications, development tools. The Zotero **Type** field names the programming language, which maps to the Schema.org `programmingLanguage` property.

### Personal Communication

- **Email** (`personal_communication`): Emails, letters, personal correspondence

---

## For Content Creators

### Choosing the Right Type

When adding an entry to the Interlisp Zotero group:

1. **Select the most specific Zotero item type** that matches your entry
   - Use `Journal Article` for peer-reviewed journal papers
   - Use `Conference Paper` for conference proceedings (not in a journal)
   - Use `Report` for technical reports and internal documentation
   - Use `Document` only when no other type fits (broad catch-all)

2. **Fill in the Type field** for the item types that use it
   - `Document`: the kind of document. Use `Transcript` for an oral-history interview.
   - `Standard`: the standard's series or designation
   - `Computer Program`: the programming language

3. **Verify your schema.org mapping** by checking this reference table

### Example: Choosing Between Report and Document

| Aspect | Report | Document |
|--------|--------|----------|
| **Best for** | Published technical reports, working papers | User manuals, specifications, guides |
| **Publisher info available** | Usually yes | Often no |
| **Formal publication** | Yes, often | Rarely |
| **Organization issuing** | Clear (government, company, academic) | May be vague |
| **Use when** | Official documentation with publication date | In-house documentation, unpublished guides |

---

## For Developers

### Processing Pipeline

The bibliography processing pipeline:

1. **Fetches data** from the Zotero API (v3) for group 2914042
2. **Extracts** the Zotero itemType and the CSL JSON type
3. **Generates markdown frontmatter** via `bibSplit.pl` (uses the CSL type)
4. **Generates JSON-LD** via the `bibliography-json-ld.html` partial (maps the CSL type to schema.org)
5. **Publishes** markdown files and embedded JSON-LD to the website

The CSL JSON type is the entry's type of record. The Zotero **Type** field is a separate thing: it is a generic classification field whose meaning depends on the item type, and Zotero's CSL export maps it to the CSL `genre` field. It never names the entry's type.

### Current Type Handling

See `layouts/_partials/bibliography-json-ld.html` for the active type mappings:

```go
{{- if eq $itemType "article-journal" -}}{{- $schemaType = "ScholarlyArticle" -}}
{{- else if eq $itemType "book" -}}{{- $schemaType = "Book" -}}
{{- else if eq $itemType "chapter" -}}{{- $schemaType = "Chapter" -}}
// ... etc
```

### Adding New Types

To add a type:

1. Add a type handler in `scripts/bibSplit.pl` (line ~143) so the pipeline emits it
2. Add the @type mapping in `layouts/_partials/bibliography-json-ld.html` (line ~25)
3. Add an `additionalType` assignment if the type needs further refinement (line ~122)
4. Add a test fixture under `tests/fixtures/bibliography/` and register its slug in `tests/conftest.py`
5. Add a test class in `tests/test_bibliography_jsonld.py`
6. Update this reference table and `docs/bibliography-schema.md`

### Known Issues

See `docs/bibliography-schema.md` for known issues and limitations in bibliography processing.

---

## Schema.org Vocabulary Notes

### CreativeWork Hierarchy

Several types map to the generic `CreativeWork` in schema.org:

- `patent` → `CreativeWork` (with `additionalType: "Patent"`)
- `document` → `CreativeWork` (with `additionalType: "TechnicalDocumentation"`)
- `document` with a `Transcript` type → `CreativeWork` (with `additionalType: "Transcript"`)
- `standard` → `CreativeWork` (with `additionalType: "Standard"`)

This hierarchy allows search engines to understand that these are creative works while providing additional specificity through `additionalType`.

### Why Not More Specific Types?

Schema.org has no native types for:
- Generic "documents"
- Transcripts (unless linked to media)
- Technical standards (as standalone documents)
- General software (though `SoftwareSourceCode` is specific)

Using `CreativeWork` with `additionalType` is the recommended schema.org pattern for these cases. Schema.org's `additionalType` documentation permits text values "sparingly, for cases where useful information can be added without their being an appropriate schema to reference", with the class label following the schema.org style guide.

### The genre Property

Schema.org's `genre` property ("Genre of the creative work") is the natural home for an entry's genre, and it is where the Zotero **Type** field is carried for `Document` entries. Both are used together for transcripts: `additionalType` states that the work is a transcript, while `genre` records the classification in schema.org's first-class slot.

The Zotero **Type** field is generic, so its meaning depends on the item type, and so does its schema.org destination:

| Zotero item type | Type field contains | Expressed in schema.org as |
|---|---|---|
| `Document` | the kind of document, e.g. `Transcript` | `genre`, plus `additionalType` |
| `Standard` | the standard's series or designation | `isPartOf` → `CreativeWorkSeries` |
| `Computer Program` | the programming language | `programmingLanguage` |
| `Report` | the report type | `additionalType` |
| `Thesis` | the degree type | `genre` |
| `Webpage` | the kind of site, e.g. `Blog` | `genre` |

---

## Troubleshooting

### Entry Not Appearing with Expected Type

1. **Check CSL JSON output**: Run `scripts/update_bibliography.sh` and examine the raw JSON for your entry's `type` field
2. **Verify mapping**: Check that the CSL type appears in the table above
3. **Check the Type field**: If the entry's `type` value looks like a genre word (for example `Transcript` or `Newsletter`) rather than a CSL type, the Zotero Type field has been populated and has overridden the entry's CSL type
4. **Report missing type**: If type is in CSL JSON but not in table, file an issue

### JSON-LD Validation Errors

1. **Use Google Structured Data Testing Tool** to validate: https://search.google.com/structured-data/testing-tool
2. **Check schema.org** for @type requirements: https://schema.org/
3. **Review generated HTML** in browser DevTools (JSON-LD is embedded in `<script type="application/ld+json">`)

---

## References

- [Zotero Item Types](https://www.zotero.org/support/kb/item_types)
- [CSL JSON Schema](https://citeproc-js.readthedocs.io/en/latest/csl-json/markup.html)
- [Schema.org Types](https://schema.org/Thing)
- [Schema.org CreativeWork](https://schema.org/CreativeWork)
- [Schema.org additionalType](https://schema.org/additionalType)
- [Schema.org genre](https://schema.org/genre)
- [Structured Data Best Practices](https://developers.google.com/search/docs/beginner/structured-data)

## Related Documentation

- [Interlisp Bibliography Intake Guide](../intake/) – How to recommend a new bibliography item
- `docs/bibliography-schema.md` – Technical details of the bibliography processing system (repository source)
