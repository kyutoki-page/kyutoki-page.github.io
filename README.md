# pages

Mirror of the public Wix viewer pages, published with GitHub Pages:

https://elemake2024-dot.github.io/pages/

The workflow in `.github/workflows/deploy-pages.yml` refreshes the public Wix sitemap and deploys its viewer pages on pushes to `main` or a `wix-published` repository dispatch event.
Editor pages are excluded. A Wix-side webhook or secure relay must send that event; without it, Wix edits are not detected automatically. This is a static mirror, not a live Wix runtime.