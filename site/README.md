# Minimal Personal Site

A text-first personal site inspired by macwright.com—fast, clean, and easy to edit.

## Edit
- Replace "Your Name" in the HTML files.
- Add posts by duplicating `/posts/hello-world.html`.
- Add links to new posts in `writing.html` and the homepage "Recently" list.
- Update `/feed.xml` with a new `<item>` per post (optional).

## Deploy (GitHub Pages)
1. Create a new public repo named `yourname.github.io`.
2. Upload the contents of this `site/` folder to the repo root.
3. In **Settings → Pages**, ensure it’s serving from the default branch.
4. Your site will be live at `https://yourname.github.io`.

## Custom Domain (optional)
- Buy a domain and add a DNS A/AAAA or CNAME record pointing to GitHub Pages.
- In the repo **Settings → Pages**, set your custom domain.

## Style tweaks
- Edit `/assets/styles.css` — typography and colors are defined with CSS variables and respect dark mode.

## No build step
Just static files. You can also host on Netlify, Cloudflare Pages, or any static host.
