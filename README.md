# Personal site

Plain HTML/CSS/JS — no build step, no dependencies.

## Edit

Open `index.html` in a text editor and replace the placeholder text
(name, bio, news, publications, experience, education, awards).
Open it directly in a browser to preview.

## Deploy with GitHub Pages (free)

1. Create a new **public** repo on GitHub, e.g. `yourname.github.io`
   (using exactly `<yourusername>.github.io` as the repo name gives you
   a root URL with no extra path; any other repo name works too, just
   served at `yourusername.github.io/reponame`).
2. From this folder:
   ```bash
   git remote add origin https://github.com/<yourusername>/<repo-name>.git
   git branch -M main
   git push -u origin main
   ```
3. On GitHub: repo → **Settings** → **Pages** → under "Build and
   deployment", set Source to **Deploy from a branch**, branch `main`,
   folder `/ (root)`. Save.
4. Your site is live in a minute or two at:
   - `https://<yourusername>.github.io` (if repo was named that way), or
   - `https://<yourusername>.github.io/<repo-name>`

## Custom domain (optional)

1. Buy a domain (Namecheap, Cloudflare, Google Domains, etc).
2. In the repo → **Settings** → **Pages** → **Custom domain**, enter your
   domain. This creates/updates the `CNAME` file in the repo for you.
3. At your domain registrar, add DNS records pointing to GitHub Pages:
   - For an apex domain (`yourname.com`): four `A` records to
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - For a `www` subdomain: a `CNAME` record to `<yourusername>.github.io`
4. Back in repo Settings → Pages, check **Enforce HTTPS** once DNS has
   propagated (can take a few minutes to a few hours).
