# pages

Live Wix viewer page embedded at a fixed GitHub Pages URL:

https://elemake2024-dot.github.io/pages/

The workflow in `.github/workflows/deploy-pages.yml` deploys `site-copy/` on pushes to `main`.
The page content is loaded directly from Wix, so published Wix changes appear without copying files. The Wix editor is not embedded.