# cwarzel.blog

A clean, minimal personal site built with Jekyll. Hosted on GitHub Pages.

## Site Structure

```
_posts/          → Blog posts (Markdown)
_photos/         → Photo entries (Markdown)
_data/log.yml    → Reading/watching/listening log
_layouts/        → Page templates
assets/          → CSS and images
  photos/        → Photo files
```

## How to Use

### Writing a Blog Post

1. Create a new file in `_posts/` named like: `2025-01-18-my-post-title.md`
2. Add front matter at the top:

```markdown
---
layout: post
title: "My Post Title"
date: 2025-01-18
---

Your content here. Write in Markdown.

Add images like this:
![Alt text](/assets/photos/my-image.jpg)
```

3. Commit and push to GitHub

### Adding Photos

1. Add your image to `assets/photos/`
2. Create a file in `_photos/` (e.g., `my-photo.md`):

```markdown
---
title: "Photo Title"
image: /assets/photos/my-photo.jpg
location: "Place, Country"
date: 2025-01-01
caption: "Optional caption"
---

Optional description text.
```

### Updating the Log

Edit `_data/log.yml` to add books, films, music:

```yaml
reading:
  - title: "Book Title"
    author: "Author Name"
    note: "Optional thoughts"

watching:
  - title: "Film or Show"
    year: 2024

listening:
  - title: "Album"
    artist: "Artist"
```

### Updating Atlantic Articles

Run this command to pull your latest articles from The Atlantic:

```bash
python update_writing.py
```

Then commit and push the changes.

## Local Development

To preview the site locally:

```bash
# Install Jekyll (one time)
gem install bundler jekyll

# Run the site
jekyll serve
```

Then visit http://localhost:4000

## Pages

- **Home** (`index.html`) - Landing page with recent posts
- **Blog** (`blog.html`) - All blog posts
- **Log** (`log.html`) - Reading/watching/listening
- **Writing** (`writing.html`) - Atlantic articles
- **Photos** (`photos.html`) - Photo gallery
- **About** (`about.html`) - Bio page

## Customization

- Edit `_config.yml` for site title, description, email
- Edit `assets/styles.css` for colors, fonts, layout
- Edit `_layouts/default.html` to change navigation
