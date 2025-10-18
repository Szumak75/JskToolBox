# Publishing JskToolBox Documentation

This guide explains how to publish the generated documentation online.

## Option 1: Read the Docs (Recommended)

### Setup

1. **Create Read the Docs Account**
   - Go to https://readthedocs.org/
   - Sign up or log in with GitHub

2. **Import Project**
   - Click "Import a Project"
   - Select JskToolBox from your repositories
   - Configuration is already in `.readthedocs.yaml`

3. **Build Documentation**
   - Read the Docs will automatically:
     - Detect the Sphinx configuration
     - Install dependencies
     - Build HTML, PDF, and EPUB
     - Host at `jsktoolbox.readthedocs.io`

### Configuration

The `.readthedocs.yaml` file is already configured with Poetry support:

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.10"
  jobs:
    pre_install:
      # Install poetry
      - pip install poetry
    post_install:
      # Install project with dev dependencies using poetry
      - poetry install --with dev

sphinx:
  configuration: docs_api/source/conf.py
  fail_on_warning: false

formats:
  - pdf
  - epub
```

**Key points**:
- Uses Poetry for dependency management
- Installs dev dependencies (including sphinx-autodoc-typehints)
- Automatically handles all Python dependencies from pyproject.toml
- Generates HTML, PDF, and EPUB formats

### Updating Documentation

Documentation rebuilds automatically on:
- Every push to main branch
- Every pull request (preview)
- Manual trigger from Read the Docs dashboard

## Option 2: GitHub Pages

### Setup

1. **Generate Documentation**
   ```bash
   make docs
   ```

2. **Create gh-pages Branch**
   ```bash
   git checkout --orphan gh-pages
   git rm -rf .
   cp -r docs_api/build/html/* .
   touch .nojekyll
   git add .
   git commit -m "Initial documentation"
   git push origin gh-pages
   ```

3. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Source: gh-pages branch
   - Documentation will be at `https://username.github.io/JskToolBox/`

### Automated Updates (GitHub Actions)

Create `.github/workflows/docs.yml`:

```yaml
name: Documentation

on:
  push:
    branches: [main, master]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install Poetry
        uses: snok/install-poetry@v1
      
      - name: Install dependencies
        run: poetry install
      
      - name: Generate documentation
        run: poetry run python generate_docs.py
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs_api/build/html
          cname: docs.yourdomain.com  # Optional: custom domain
```

## Option 3: Self-Hosted

### Using Python HTTP Server

```bash
# Generate documentation
make docs

# Serve locally
cd docs_api/build/html
python -m http.server 8000

# Access at http://localhost:8000
```

### Using Nginx

```nginx
server {
    listen 80;
    server_name docs.yourdomain.com;
    
    root /path/to/JskToolBox/docs_api/build/html;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Using Apache

```apache
<VirtualHost *:80>
    ServerName docs.yourdomain.com
    DocumentRoot /path/to/JskToolBox/docs_api/build/html
    
    <Directory /path/to/JskToolBox/docs_api/build/html>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>
```

## Option 4: GitLab Pages

### .gitlab-ci.yml

```yaml
pages:
  stage: deploy
  image: python:3.10
  before_script:
    - pip install poetry
    - poetry install
  script:
    - poetry run python generate_docs.py
    - mv docs_api/build/html public
  artifacts:
    paths:
      - public
  only:
    - main
```

## Option 5: Netlify

### Setup

1. **Connect Repository**
   - Go to https://netlify.com
   - Click "New site from Git"
   - Select JskToolBox repository

2. **Configure Build**
   - Build command: `poetry install && poetry run python generate_docs.py`
   - Publish directory: `docs_api/build/html`

3. **Deploy**
   - Netlify will automatically deploy on push
   - Access at `https://jsktoolbox.netlify.app`

### netlify.toml

```toml
[build]
  command = "poetry install && poetry run python generate_docs.py"
  publish = "docs_api/build/html"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## Option 6: Vercel

### Setup

1. **Import Project**
   - Go to https://vercel.com
   - Import JskToolBox repository

2. **Configure**
   - Build Command: `poetry install && poetry run python generate_docs.py`
   - Output Directory: `docs_api/build/html`

### vercel.json

```json
{
  "buildCommand": "poetry install && poetry run python generate_docs.py",
  "outputDirectory": "docs_api/build/html",
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ]
}
```

## Comparison

| Platform | Pros | Cons | Best For |
|----------|------|------|----------|
| **Read the Docs** | Free, automatic, PDF/EPUB, versioning | Requires account | Open source projects |
| **GitHub Pages** | Free, integrated with GitHub | Manual setup | GitHub-hosted projects |
| **Self-Hosted** | Full control, no limitations | Requires server management | Corporate/private |
| **GitLab Pages** | Free CI/CD integration | GitLab only | GitLab users |
| **Netlify** | Easy setup, CDN | Free tier limits | Quick deployment |
| **Vercel** | Fast builds, edge network | Free tier limits | Modern stack projects |

## Custom Domain

### Read the Docs

1. Go to Admin → Domains
2. Add your domain (e.g., `docs.yourdomain.com`)
3. Configure DNS:
   ```
   CNAME docs.yourdomain.com jsktoolbox.readthedocs.io
   ```

### GitHub Pages

1. Add `CNAME` file to gh-pages branch:
   ```
   docs.yourdomain.com
   ```
2. Configure DNS:
   ```
   CNAME docs.yourdomain.com username.github.io
   ```

### Netlify/Vercel

1. Go to domain settings
2. Add custom domain
3. Follow DNS configuration instructions

## SSL/HTTPS

- **Read the Docs**: Automatic HTTPS
- **GitHub Pages**: Automatic HTTPS
- **Netlify/Vercel**: Automatic HTTPS
- **Self-Hosted**: Use Let's Encrypt:
  ```bash
  certbot --nginx -d docs.yourdomain.com
  ```

## Versioning

### Read the Docs

Automatically supports versioning:
- Latest (main branch)
- Stable (latest release)
- Specific versions (tags)

### Manual Versioning

```bash
# Generate docs for version 1.0
git checkout v1.0
make docs
mv docs_api/build/html docs_api/build/v1.0

# Generate docs for version 2.0
git checkout v2.0
make docs
mv docs_api/build/html docs_api/build/v2.0

# Create index
cat > docs_api/build/index.html <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>JskToolBox Documentation</title>
</head>
<body>
    <h1>JskToolBox Documentation</h1>
    <ul>
        <li><a href="v2.0/index.html">Version 2.0 (Latest)</a></li>
        <li><a href="v1.0/index.html">Version 1.0</a></li>
    </ul>
</body>
</html>
EOF
```

## Updating Documentation

### Automatic (Recommended)

Set up CI/CD (GitHub Actions, GitLab CI, etc.) to:
1. Trigger on push to main
2. Generate documentation
3. Deploy to hosting platform

### Manual

```bash
# Update documentation
git pull
make docs

# For Read the Docs
# Just push to GitHub - automatic rebuild

# For GitHub Pages
git checkout gh-pages
cp -r docs_api/build/html/* .
git add .
git commit -m "Update documentation"
git push origin gh-pages

# For self-hosted
rsync -avz docs_api/build/html/ user@server:/path/to/docs/
```

## Best Practices

1. **Automate**: Use CI/CD for automatic updates
2. **Version**: Support multiple versions if needed
3. **SSL**: Always use HTTPS
4. **CDN**: Use platform with CDN for speed
5. **Search**: Enable search functionality
6. **Analytics**: Add Google Analytics or similar
7. **Sitemap**: Generate sitemap for SEO
8. **Robots.txt**: Configure for search engines

## Monitoring

### Read the Docs

- Built-in analytics
- Build logs
- Traffic statistics

### Self-Hosted

Add to HTML (`docs_api/source/conf.py`):

```python
# Google Analytics
html_theme_options = {
    'analytics_id': 'G-XXXXXXXXXX',
}

# Or add custom HTML
html_js_files = [
    ('https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX', {'async': 'async'}),
]
```

## Troubleshooting

### Build Fails

1. Check Python version (3.10+)
2. Verify dependencies installed
3. Check Sphinx configuration
4. Review build logs

### Missing Modules

1. Ensure all modules have docstrings
2. Check RST files exist
3. Verify module paths in conf.py
4. Check exclude patterns

### Broken Links

1. Run link checker:
   ```bash
   cd docs_api
   poetry run make linkcheck
   ```
2. Fix broken references
3. Rebuild documentation

## Support

- **Read the Docs**: https://docs.readthedocs.io/
- **GitHub Pages**: https://docs.github.com/pages
- **Sphinx**: https://www.sphinx-doc.org/

---

**Recommendation**: Start with Read the Docs for ease of use and features. Switch to GitHub Pages or self-hosted if you need more control.
