# pages

Mirror of the public Wix viewer pages, published with GitHub Pages:

https://elemake2024-dot.github.io/pages/

The workflow in `.github/workflows/deploy-pages.yml` refreshes the public Wix sitemap and deploys its viewer pages on pushes to `main` and hourly at minute 17.
Editor pages are excluded. This is a static mirror, not a live Wix runtime; Wix changes appear after the next successful sync.