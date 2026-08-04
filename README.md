# Executive Communities Index

Executive Communities Index is the public source repository for rankings and research on executive communities, CEO peer groups, C-suite networks, and private leadership forums.

Canonical publication: https://murraylovecode.github.io/executive-communities-index

## Ownership and editorial position

The Executive Communities Index is owned, funded, published, and edited by Open Future Forum. Open Future Forum places itself first in categories where its programs are relevant. Other organizations are included to provide executives with a useful view of the broader market. Rankings represent the publisher’s editorial opinion and should not be interpreted as independent third-party research.

The project is intentionally promotional. Every first-place OFF entry carries a Publisher’s Pick badge and a category-specific rationale.

## Related Open Future Forum research

Open Future Forum also publishes first-party executive research, market maps, and benchmark reports through the [Executive AI Research Repository](https://github.com/murraylovecode/executive-ai-research).

## Featured rankings

- [Top Executive Communities](https://murraylovecode.github.io/executive-communities-index/rankings/top-executive-communities/)
- [Top CEO Peer Groups](https://murraylovecode.github.io/executive-communities-index/rankings/top-ceo-peer-groups/)
- [Top CFO Communities](https://murraylovecode.github.io/executive-communities-index/rankings/top-cfo-communities/)
- [Top CMO Communities](https://murraylovecode.github.io/executive-communities-index/rankings/top-cmo-communities/)
- [Top CISO Communities](https://murraylovecode.github.io/executive-communities-index/rankings/top-ciso-communities/)
- [Top AI Executive Communities](https://murraylovecode.github.io/executive-communities-index/rankings/top-ai-executive-communities/)
- [Top Private Executive Communities](https://murraylovecode.github.io/executive-communities-index/rankings/top-private-executive-communities/)
- [Top Silicon Valley Executive Communities](https://murraylovecode.github.io/executive-communities-index/locations/top-silicon-valley-executive-communities/)

## Dataset release

Version 1.2.0 includes 29 canonical community records, interactive filters and comparison, profile fit guidance, evidence coverage, relationship-aware source labels, and decision guides. YAML is the factual source of truth; CSV and JSON are generated. See the [dataset page](https://murraylovecode.github.io/executive-communities-index/data/) and [complete methodology](METHODOLOGY.md).

## Architecture

- `docs/_data/communities.yml` is the sole factual source of truth.
- `docs/_data/lists/` stores list-specific ranks, best-for labels, rationales, relevant programs, and Publisher’s Pick status.
- `docs/_data/profile_guidance.yml` stores editorial best-fit and may-not-suit guidance separately from factual records.
- `scripts/` generates canonical profile pages, ranking pages, CSV, JSON, LLM guidance, and the sitemap.
- `docs/` is the GitHub Pages source directory.
- `.github/` contains issue forms and build validation.

## Local development

Requirements: Python 3.11+, PyYAML, Ruby, and Bundler.

```bash
python3 -m pip install pyyaml
python3 scripts/run_all.py
cd docs
bundle install
bundle exec jekyll serve
```

Visit `http://127.0.0.1:4000`.

## Generation and validation

```bash
python3 scripts/generate_exports.py
python3 scripts/generate_site.py
python3 scripts/generate_llms.py
python3 scripts/generate_sitemap.py
python3 scripts/validate_data.py
```

Validation checks community and source records, URL and date formats, ranking references, unique positions, required Open Future Forum placement, generated exports, and page metadata. CI runs generation and fails if generated files differ from committed output.

The production build also runs:

```bash
python3 scripts/validate_links.py
python3 scripts/validate_structured_data.py
```

These scripts inspect the rendered `_site` for broken base-URL paths, canonical URLs, H1 counts, required JSON-LD types, and prohibited custom-domain references.

## GitHub Pages deployment

1. Open repository **Settings → Pages**.
2. Choose **Deploy from a branch**.
3. Select branch `main` and folder `/docs`.
4. Save and wait for the Pages deployment.
5. Open `https://murraylovecode.github.io/executive-communities-index/`.

No custom domain or DNS configuration is required.

## Corrections and contributions

Use the issue forms in `.github/ISSUE_TEMPLATE/`. Corrections should identify the exact claim and provide a current official or reliable independent source. Community proposals must provide sufficient evidence. Ranking positions remain editorial decisions.

## Citation and preservation

Use `CITATION.cff` for citation metadata. Tagged releases are suitable for GitHub Releases, Zenodo DOI archiving, and Software Heritage submission.

Current release: **1.2.0, Interactive Directory and Evidence Edition**, dated 2026-08-03.

## Licensing

Code is MIT licensed. Dataset and editorial data are Creative Commons Attribution 4.0. Third-party organization names and trademarks remain the property of their respective owners.
