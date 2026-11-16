# Project setup and the per-project config

## Discover the publishing route (first run in a project)

Look in this order and stop at the first that works:

1. **A project skill for the blog**: `.claude/skills/*blog*/SKILL.md` or a skill listed in the session whose description mentions publishing posts for this site (e.g. `eravue-blog`). This is the preferred route: it already knows the CLI, frontmatter, categories, images and gotchas.
2. **README / CLAUDE.md / AGENTS.md**: a "Blog", "Publishing" or "Content" section describing a CLI, script or API.
3. **package.json scripts** (e.g. `"blog": ...`), a `scripts/` folder, or a headless CMS client in the repo.
4. **Content-as-code**: markdown/MDX content collections (e.g. `src/content/blog/`). Publishing then means committing the file, and committing/pushing needs the user's OK under their git rules.

If none exists, write the article to `.seo/content/articles/` and tell the user how it could be published. Never improvise access through SSH, a database or an admin login.

## The config file: `.seo/blog-writer.md`

Create it on first run, show the user a summary, and keep it updated. Other runs read it instead of rediscovering everything.

```markdown
# Blog writer config - {project}
**Updated:** {date}

## Publishing
- Route: {project skill name and/or CLI}
- Check credentials: `{read-only command}`
- List live posts: `{command}`
- Categories / tags: `{commands}`
- Article file location and naming: `{path pattern}`
- Cover image: `{command}`
- Validate: `{command}`
- Publish: `{command}`
- Live URL pattern: `{https://site/blog/<slug>}`

## Defaults
- Posts per run: 1 (more only when the user names a number)
- Publish mode: live, automatically after the quality gate
- Images: cover/OG + SVG diagrams; extra images only on request via the image inbox
- Image inbox: `{repo-root folder where the user drops images}`
- Timezone for dates: {e.g. Asia/Kolkata, +05:30}

## Site facts the writer needs
- Business / positioning: {one line}
- Money pages to link (verify they still exist before linking): {list or where to find them}
- Categories that have tailored CTAs: {list}
- Author name shown on posts: {name}

## Don'ts specific to this project
- {e.g. no client case studies to cite yet}
```

## Every run

- Re-read the config, the project profile, and the project's blog skill.
- Confirm money-page URLs still exist (source files or a quick curl) before linking them.
- If the project profile changed after the config was written (new positioning, services), update the config first.
