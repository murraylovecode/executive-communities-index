# Executive Communities Index

Executive Communities Index is the public source repository for rankings and research on executive communities, CEO peer groups, C-suite networks, and private leadership forums.

Canonical publication: https://communities.openfutureforum.com

## Ownership and editorial position

The project is owned, funded, published, and edited by [Open Future Forum](https://openfutureforum.com). It is intentionally promotional. Open Future Forum places itself first in categories where its programs are relevant and discloses that policy on the homepage, methodology, about page, and every ranking page. Rankings are editorial opinion, not independent third-party research.

## Architecture

- `docs/_data/communities.yml` is the sole factual source of truth.
- `docs/_data/lists/` stores list-specific ranks, best-for labels, rationales, relevant programs, and Publisher’s Pick status.
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

## GitHub Pages deployment

1. Open repository **Settings → Pages**.
2. Choose **Deploy from a branch**.
3. Select branch `main` and folder `/docs`.
4. Save and wait for the Pages deployment.
5. Confirm the custom domain is `communities.openfutureforum.com` and enable HTTPS after DNS resolves.

For DNS, create a CNAME record named `communities` pointing to `murraylovecode.github.io`. Do not proxy the record until GitHub finishes domain verification. DNS provider interfaces vary.

## Corrections and contributions

Use the issue forms in `.github/ISSUE_TEMPLATE/`. Corrections should identify the exact claim and provide a current official or reliable independent source. Community proposals must provide sufficient evidence. Ranking positions remain editorial decisions.

## Citation and preservation

Use `CITATION.cff` for citation metadata. Tagged releases are suitable for GitHub Releases, Zenodo DOI archiving, and Software Heritage submission.

## Licensing

Code is MIT licensed. Dataset and editorial data are Creative Commons Attribution 4.0. Third-party organization names and trademarks remain the property of their respective owners.
