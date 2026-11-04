# Profile refresh notes

- The README deliberately retains the original FSF statement, X-Men GIF, and satirical badges.
- Technology labels use Shields.io static badges, avoiding nonexistent icon file paths. If a brand logo isn't supported by Shields.io, its technology name still renders.
- The GitHub metrics SVG is generated weekly and on demand by `lowlighter/metrics`, then committed to `assets/github-metrics.svg` on `main`.
- After merging the PR, run **Actions → Update profile metrics → Run workflow** once. Until that run completes, the metrics image will not exist.
- Repository Actions must have permission to write contents. Check **Settings → Actions → General → Workflow permissions** if the commit fails.
- The workflow uses the built-in `GITHUB_TOKEN`; private repositories or additional private activity may require a separately configured, appropriately scoped token.
- Avoid including secrets in SVGs or workflow logs. The workflow is not executed from this draft PR.
- External GIF and Shields.io images remain externally hosted; they can still be affected by third-party outages.
