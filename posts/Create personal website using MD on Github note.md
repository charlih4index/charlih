---
title: "Create personal website using MD on Github note"
date: 2026-09-20
authors:
  - name: Charlih Chen
    email: charlih_chen@hotmail.com
    orcid: 0000-0001-5437-4073
    url: https://charlih.com
description: Create personal website using MD on Github note.
thumbnail: https://charlih.com/thumbnail/thumbnail1.jpg
tags:
  - MyST Markdown
  - GitHub Template
  - GitHub Actions
  - Pre-commit
keywords:
  - MyST Markdown
  - GitHub Template
  - GitHub Actions
  - Pre-commit
---

# Note for Building Websites with MyST Markdown on Github

## Q1: The custom domain via CNAME is not working even updated the DNS on purchased povider?

## A1: 

If you configure a custom domain (via CNAME), remove AKA using # to mark the BASE_URL environment variable from deploy.yml 

charlihchen/charlih/CNAME : charlih.com

charlihchen/charlih/.gitHub/workflows/deploy.yml

```diff
.....
      - name: Build HTML Assets
        # Remove BASE_URL if using a custom domain (CNAME)
-       # env:
-        # BASE_URL: /${{ github.event.repository.name }}
        run: myst build --html
.....
```

## Q2: Why there is no Banner, Primary Sidebar, Secondary Sidebar, Website Header, Website Footer section areas?
## A2:

Have to enable the personal website repository on Github from "Settings" >> "Pages" >> select "GitHub Actions" under "Build and deployment" section


