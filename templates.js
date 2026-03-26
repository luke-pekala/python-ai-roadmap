// templates.js — DocStruct Template Definitions
// Each template has: label, fields[], and generate(data)

const TEMPLATES = {

  // ─────────────────────────────────────────────────────────
  api_reference: {
    label: "API Reference",
    fields: [
      { id: "api_name",       label: "API Name",           placeholder: "e.g. Payment Gateway API",          required: true  },
      { id: "version",        label: "Version",             placeholder: "e.g. v2.1.0",                       required: true  },
      { id: "base_url",       label: "Base URL",            placeholder: "e.g. https://api.example.com/v2",   required: true  },
      { id: "description",    label: "Description",         placeholder: "What this API does in 1–2 sentences", required: true  },
      { id: "auth_method",    label: "Auth Method",         placeholder: "e.g. Bearer token, API key, OAuth 2.0", required: true  },
      { id: "auth_header",    label: "Auth Header/Param",   placeholder: "e.g. Authorization: Bearer <token>", required: false },
      { id: "endpoint_name",  label: "Primary Endpoint",    placeholder: "e.g. POST /users",                  required: false },
      { id: "author",         label: "Author",              placeholder: "e.g. Platform Team",                required: false },
    ],
    generate(data) {
      const today = new Date().toISOString().split("T")[0];
      return `# ${data.api_name || "API Name"} Reference

**Version:** ${data.version || "v1.0.0"}
**Base URL:** \`${data.base_url || "https://api.example.com"}\`
**Last Updated:** ${today}
**Author:** ${data.author || "Documentation Team"}

---

## Overview

${data.description || "Provide a 1–2 sentence description of what this API does and who it is for."}

### Key Features

- Feature one
- Feature two
- Feature three

### Prerequisites

- Prerequisite one
- Prerequisite two

---

## Authentication

This API uses **${data.auth_method || "token-based authentication"}**.

${data.auth_header
  ? `Include the following in every request header:\n\n\`\`\`\n${data.auth_header}\n\`\`\``
  : `Include your credentials in every request header:\n\n\`\`\`\nAuthorization: Bearer <your_token>\n\`\`\``
}

### Obtaining Credentials

1. Step one to get credentials
2. Step two to get credentials
3. Step three to get credentials

### Token Expiry

Describe token lifetime and refresh behaviour here.

---

## Endpoints

### ${data.endpoint_name || "POST /resource"}

Brief description of what this endpoint does.

**Request**

\`\`\`http
${data.endpoint_name || "POST /resource"} HTTP/1.1
Host: ${(data.base_url || "https://api.example.com").replace(/https?:\/\//, "").split("/")[0]}
${data.auth_header || "Authorization: Bearer <token>"}
Content-Type: application/json
\`\`\`

---

## Parameters

### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| \`param_one\` | string | Yes | Description of param_one |
| \`param_two\` | integer | No | Description of param_two |
| \`param_three\` | boolean | No | Description of param_three |

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| \`page\` | integer | 1 | Page number for pagination |
| \`limit\` | integer | 20 | Number of results per page |

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| \`{id}\` | string | Unique identifier of the resource |

---

## Response

### Success Response — 200 OK

\`\`\`json
{
  "status": "success",
  "data": {
    "id": "abc123",
    "field_one": "value",
    "field_two": 42,
    "created_at": "2024-01-15T10:30:00Z"
  },
  "meta": {
    "page": 1,
    "total": 100
  }
}
\`\`\`

### Error Responses

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| \`400\` | Bad Request | Missing or invalid parameters |
| \`401\` | Unauthorized | Invalid or expired credentials |
| \`403\` | Forbidden | Insufficient permissions |
| \`404\` | Not Found | Resource does not exist |
| \`429\` | Too Many Requests | Rate limit exceeded |
| \`500\` | Internal Server Error | Unexpected server-side error |

### Error Response Body

\`\`\`json
{
  "status": "error",
  "code": "INVALID_PARAMETER",
  "message": "Human-readable error description",
  "details": {}
}
\`\`\`

---

## Examples

### Example 1 — Basic Request

\`\`\`bash
curl -X POST \\
  ${data.base_url || "https://api.example.com"}/resource \\
  -H "${data.auth_header || "Authorization: Bearer <token>"}" \\
  -H "Content-Type: application/json" \\
  -d '{
    "param_one": "value",
    "param_two": 42
  }'
\`\`\`

### Example 2 — With Optional Parameters

\`\`\`bash
curl -X GET \\
  "${data.base_url || "https://api.example.com"}/resource?page=2&limit=50" \\
  -H "${data.auth_header || "Authorization: Bearer <token>"}"
\`\`\`

### Example 3 — Handling the Response (JavaScript)

\`\`\`javascript
const response = await fetch("${data.base_url || "https://api.example.com"}/resource", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "${data.auth_method || "Authorization"}: Bearer <token>"
  },
  body: JSON.stringify({ param_one: "value" })
});

const json = await response.json();
console.log(json.data);
\`\`\`

---

## Rate Limits

| Tier | Requests per minute |
|------|---------------------|
| Free | 60 |
| Pro | 600 |
| Enterprise | Unlimited |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| ${data.version || "v1.0.0"} | ${today} | Initial release |
`;
    }
  },


  // ─────────────────────────────────────────────────────────
  user_manual: {
    label: "User Manual",
    fields: [
      { id: "product_name",   label: "Product Name",       placeholder: "e.g. Acme Dashboard",               required: true  },
      { id: "version",        label: "Product Version",     placeholder: "e.g. 3.4.0",                        required: true  },
      { id: "audience",       label: "Target Audience",     placeholder: "e.g. End users, admins",            required: true  },
      { id: "description",    label: "Product Description", placeholder: "What this product does",            required: true  },
      { id: "platform",       label: "Platform/OS",         placeholder: "e.g. Web, Windows 10+, macOS 12+",  required: false },
      { id: "support_email",  label: "Support Email",       placeholder: "e.g. support@example.com",         required: false },
      { id: "author",         label: "Author",              placeholder: "e.g. Product Documentation Team",  required: false },
    ],
    generate(data) {
      const today = new Date().toISOString().split("T")[0];
      return `# ${data.product_name || "Product Name"} User Manual

**Version:** ${data.version || "1.0.0"}
**Platform:** ${data.platform || "Web / Desktop / Mobile"}
**Audience:** ${data.audience || "End Users"}
**Last Updated:** ${today}
**Author:** ${data.author || "Documentation Team"}

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Installation & Setup](#installation--setup)
4. [User Interface Overview](#user-interface-overview)
5. [Core Features](#core-features)
6. [Settings & Preferences](#settings--preferences)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)
9. [Support & Contact](#support--contact)

---

## Introduction

${data.description || "Describe what this product does and what problem it solves for the user."}

### Who This Manual Is For

This manual is intended for **${data.audience || "end users"}** who want to get the most out of ${data.product_name || "this product"}.

### What You Will Learn

- How to set up and configure ${data.product_name || "the product"}
- How to use the core features
- How to customise your experience
- How to resolve common issues

---

## Getting Started

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS | ${data.platform || "Windows 10 / macOS 11"} | Latest version |
| RAM | 4 GB | 8 GB |
| Disk Space | 500 MB | 2 GB |
| Internet | Required | Broadband |

### Quick Start

1. **Step one** — Describe the first thing a new user must do
2. **Step two** — Describe the second step
3. **Step three** — Describe the third step
4. You are now ready to use ${data.product_name || "the product"}

---

## Installation & Setup

### Download

Describe where and how to download the product.

### Installation Steps

1. Run the installer
2. Accept the licence agreement
3. Choose install location
4. Click Install
5. Launch ${data.product_name || "the application"}

### First-Time Configuration

Walk the user through initial configuration steps here.

---

## User Interface Overview

### Main Screen

Describe the main screen and its key areas. Add a screenshot reference here.

> **Screenshot:** Main dashboard overview

### Navigation

Explain the primary navigation elements (sidebar, top bar, menus).

### Key UI Elements

| Element | Location | Purpose |
|---------|----------|---------|
| Element one | Top bar | Description |
| Element two | Sidebar | Description |
| Element three | Main area | Description |

---

## Core Features

### Feature One

**What it does:** Describe the feature.

**How to use it:**

1. Step one
2. Step two
3. Step three

> 💡 **Tip:** Add a helpful tip about this feature.

---

### Feature Two

**What it does:** Describe the feature.

**How to use it:**

1. Step one
2. Step two
3. Step three

---

### Feature Three

**What it does:** Describe the feature.

**How to use it:**

1. Step one
2. Step two
3. Step three

---

## Settings & Preferences

### Accessing Settings

Explain how to open the settings panel.

### General Settings

| Setting | Options | Default | Description |
|---------|---------|---------|-------------|
| Setting one | On / Off | On | Description |
| Setting two | List of options | Default value | Description |

### Account Settings

Describe account-level settings here.

---

## Troubleshooting

### Common Issues

**Problem:** Describe a common problem.
**Solution:** Describe the fix step by step.

---

**Problem:** Describe another common problem.
**Solution:** Describe the fix.

---

**Problem:** Describe a third common problem.
**Solution:** Describe the fix.

---

## FAQ

**Q: Frequently asked question one?**
A: Answer here.

**Q: Frequently asked question two?**
A: Answer here.

**Q: Frequently asked question three?**
A: Answer here.

---

## Support & Contact

If you cannot resolve your issue using this manual:

- **Email:** ${data.support_email || "support@example.com"}
- **Help Centre:** https://help.example.com
- **Community Forum:** https://community.example.com

**Response times:** Weekdays, 9am–5pm. Replies within 1 business day.
`;
    }
  },


  // ─────────────────────────────────────────────────────────
  release_notes: {
    label: "Release Notes",
    fields: [
      { id: "product_name",   label: "Product Name",        placeholder: "e.g. Acme Dashboard",              required: true  },
      { id: "version",        label: "Version Number",       placeholder: "e.g. 4.2.0",                       required: true  },
      { id: "release_date",   label: "Release Date",         placeholder: "e.g. 2024-06-15",                  required: true  },
      { id: "release_type",   label: "Release Type",         placeholder: "e.g. Major, Minor, Patch, Hotfix", required: false },
      { id: "summary",        label: "Release Summary",      placeholder: "One sentence describing this release", required: true  },
      { id: "author",         label: "Author",               placeholder: "e.g. Engineering Team",            required: false },
    ],
    generate(data) {
      return `# ${data.product_name || "Product Name"} — Release Notes

## Version ${data.version || "X.Y.Z"} — ${data.release_type || "Release"}

**Release Date:** ${data.release_date || new Date().toISOString().split("T")[0]}
**Type:** ${data.release_type || "Minor Release"}
**Prepared by:** ${data.author || "Engineering Team"}

---

## Summary

${data.summary || "Describe the overall purpose and focus of this release in one or two sentences."}

---

## What's New

### ✨ New Features

- **Feature name** — Description of the new feature and its benefit to users.
- **Feature name** — Description of the new feature and its benefit to users.
- **Feature name** — Description of the new feature and its benefit to users.

---

## Improvements

### ⚡ Performance

- Improvement description — include measurable impact where possible (e.g. "50% faster load time")
- Improvement description

### 🎨 UI / UX

- UI change description
- UI change description

### 🔧 Developer Experience

- DX improvement description
- DX improvement description

---

## Bug Fixes

| # | Component | Description | Severity |
|---|-----------|-------------|----------|
| 1 | Component name | Description of the bug that was fixed | High |
| 2 | Component name | Description of the bug that was fixed | Medium |
| 3 | Component name | Description of the bug that was fixed | Low |

---

## Breaking Changes

> ⚠️ **Action required if upgrading from a previous version.**

### Breaking Change One

**What changed:** Describe what changed.
**Why:** Reason for the breaking change.
**Migration steps:**

1. Step one
2. Step two
3. Step three

---

## Deprecations

The following features are deprecated in this release and will be removed in a future version:

| Feature | Deprecated Since | Removal Version | Replacement |
|---------|-----------------|-----------------|-------------|
| Feature name | ${data.version || "X.Y.Z"} | X.Y+2.Z | Replacement feature |

---

## Known Issues

| # | Description | Workaround | Expected Fix |
|---|-------------|------------|--------------|
| 1 | Known issue description | Workaround steps | vX.Y+1.Z |

---

## Upgrade Instructions

### From Previous Version

\`\`\`bash
# Add upgrade commands here
npm install ${(data.product_name || "package-name").toLowerCase().replace(/\s+/g, "-")}@${data.version || "latest"}
\`\`\`

### Data Migration

Describe any database or data migration steps required.

---

## Compatibility

| Dependency | Required Version |
|------------|-----------------|
| Dependency one | >= X.Y.Z |
| Dependency two | >= X.Y.Z |

---

## Acknowledgements

Thanks to the following contributors for this release: [Contributor names]

---

*For questions about this release, contact ${data.author || "the engineering team"}.*
`;
    }
  },


  // ─────────────────────────────────────────────────────────
  how_to_guide: {
    label: "How-To Guide",
    fields: [
      { id: "task_name",      label: "Task Name",           placeholder: "e.g. Set up two-factor authentication", required: true  },
      { id: "product_name",   label: "Product/System",      placeholder: "e.g. Acme Dashboard",                   required: true  },
      { id: "audience",       label: "Audience",            placeholder: "e.g. Admin users, developers",          required: true  },
      { id: "time_required",  label: "Time Required",       placeholder: "e.g. 10 minutes",                       required: false },
      { id: "difficulty",     label: "Difficulty",          placeholder: "e.g. Beginner, Intermediate, Advanced", required: false },
      { id: "prerequisites",  label: "Prerequisites",       placeholder: "e.g. Admin account, Node.js installed", required: false },
      { id: "author",         label: "Author",              placeholder: "e.g. Platform Team",                    required: false },
    ],
    generate(data) {
      const today = new Date().toISOString().split("T")[0];
      return `# How To: ${data.task_name || "Complete Task Name"}

**Product:** ${data.product_name || "Product / System"}
**Audience:** ${data.audience || "All users"}
**Difficulty:** ${data.difficulty || "Intermediate"}
**Time Required:** ${data.time_required || "15 minutes"}
**Last Updated:** ${today}
**Author:** ${data.author || "Documentation Team"}

---

## Overview

This guide explains how to **${data.task_name || "complete this task"}** in ${data.product_name || "the product"}.

By the end of this guide you will be able to:

- Outcome one
- Outcome two
- Outcome three

---

## Before You Begin

### Prerequisites

${data.prerequisites
  ? data.prerequisites.split(",").map(p => `- ${p.trim()}`).join("\n")
  : `- Prerequisite one\n- Prerequisite two\n- Prerequisite three`
}

### What You Will Need

- Item or access required
- Item or access required
- Item or access required

> ⚠️ **Important:** Add any critical warnings the user must read before starting.

---

## Steps

### Step 1 — [Action Verb + Object]

Describe exactly what the user needs to do in this step. Be specific. Use present tense and active voice.

\`\`\`
# Code or command for this step, if applicable
\`\`\`

> 💡 **Tip:** Add a helpful tip that makes this step easier.

---

### Step 2 — [Action Verb + Object]

Describe exactly what the user needs to do in this step.

\`\`\`
# Code or command for this step, if applicable
\`\`\`

**Expected result:** Describe what the user should see or what should happen after completing this step.

---

### Step 3 — [Action Verb + Object]

Describe exactly what the user needs to do in this step.

---

### Step 4 — [Action Verb + Object]

Describe exactly what the user needs to do in this step.

---

### Step 5 — [Action Verb + Object]

Describe exactly what the user needs to do in this step.

**Expected result:** Describe the final outcome confirming the task is complete.

---

## Verification

After completing all steps, verify success:

1. Verification step one — what to check
2. Verification step two — what to check
3. Verification step three — what to confirm

✅ If you see [expected outcome], the task is complete.

---

## Troubleshooting

### Problem: [Common error or issue]

**Cause:** Why this happens.
**Solution:**
1. Fix step one
2. Fix step two

---

### Problem: [Another common issue]

**Cause:** Why this happens.
**Solution:** How to resolve it.

---

## Related Guides

- [Related guide one](link)
- [Related guide two](link)
- [Related guide three](link)
`;
    }
  },


  // ─────────────────────────────────────────────────────────
  troubleshooting: {
    label: "Troubleshooting Guide",
    fields: [
      { id: "product_name",   label: "Product/System Name", placeholder: "e.g. Acme Dashboard",              required: true  },
      { id: "component",      label: "Component/Area",      placeholder: "e.g. Authentication, Payments, API", required: true  },
      { id: "audience",       label: "Audience",            placeholder: "e.g. End users, support agents",    required: true  },
      { id: "version",        label: "Product Version",     placeholder: "e.g. 4.x",                          required: false },
      { id: "support_email",  label: "Escalation Contact",  placeholder: "e.g. support@example.com",          required: false },
      { id: "author",         label: "Author",              placeholder: "e.g. Support Engineering",          required: false },
    ],
    generate(data) {
      const today = new Date().toISOString().split("T")[0];
      return `# Troubleshooting Guide — ${data.component || "Component Name"}

**Product:** ${data.product_name || "Product Name"} ${data.version ? `(${data.version})` : ""}
**Component:** ${data.component || "Component / Feature Area"}
**Audience:** ${data.audience || "Support agents and advanced users"}
**Last Updated:** ${today}
**Author:** ${data.author || "Support Engineering"}

---

## How to Use This Guide

1. Find the error message or symptom that matches your situation
2. Follow the diagnostic steps in order — do not skip steps
3. If a step resolves the issue, stop. You do not need to continue.
4. If all steps fail, escalate using the contact at the end of this guide.

---

## Quick Diagnostic Checklist

Before diving into specific issues, check the following:

- [ ] Is the service showing any active incidents? Check the [status page](https://status.example.com)
- [ ] Are you on a supported version? (Supported: ${data.version || "latest two major versions"})
- [ ] Have you cleared your browser cache and cookies?
- [ ] Do you have the required permissions for this action?
- [ ] Is your network connection stable?

---

## Issue Index

| # | Symptom | Section |
|---|---------|---------|
| 1 | [Error message or symptom one] | [Issue 1](#issue-1--error-message-or-symptom) |
| 2 | [Error message or symptom two] | [Issue 2](#issue-2--error-message-or-symptom) |
| 3 | [Error message or symptom three] | [Issue 3](#issue-3--error-message-or-symptom) |
| 4 | [Error message or symptom four] | [Issue 4](#issue-4--error-message-or-symptom) |
| 5 | [Error message or symptom five] | [Issue 5](#issue-5--error-message-or-symptom) |

---

## Issue 1 — [Error Message or Symptom]

**Severity:** High / Medium / Low
**Affected versions:** ${data.version || "All versions"}
**Frequency:** Common / Occasional / Rare

### Symptoms

- Describe exactly what the user sees or experiences
- Include any error codes or messages verbatim

### Probable Causes

1. Most likely cause
2. Second likely cause
3. Less likely cause

### Diagnostic Steps

**Step 1 — Check [X]**

Describe what to check and how.

\`\`\`
# Command or code to run diagnostics, if applicable
\`\`\`

**Expected output:** Describe what a healthy result looks like.
**If you see [bad output]:** Proceed to Step 2.
**If you see [good output]:** This is not the cause — skip to Step 3.

---

**Step 2 — [Corrective Action]**

Describe the fix.

\`\`\`
# Command or configuration change
\`\`\`

**Result:** Describe what should happen after applying this fix.

---

**Step 3 — [Alternative Fix]**

Describe an alternative resolution path.

### Resolution

✅ The issue is resolved when: [describe the expected state after successful resolution].

---

## Issue 2 — [Error Message or Symptom]

**Severity:** High / Medium / Low

### Symptoms

- Symptom description

### Probable Causes

1. Probable cause one
2. Probable cause two

### Diagnostic Steps

**Step 1 —** Description of diagnostic step.

**Step 2 —** Description of corrective action.

### Resolution

✅ The issue is resolved when: [expected resolved state].

---

## Issue 3 — [Error Message or Symptom]

**Severity:** High / Medium / Low

### Symptoms

- Symptom description

### Diagnostic Steps

**Step 1 —** Diagnostic step description.

**Step 2 —** Fix description.

### Resolution

✅ The issue is resolved when: [expected resolved state].

---

## Issue 4 — [Error Message or Symptom]

**Severity:** High / Medium / Low

### Symptoms

- Symptom description

### Diagnostic Steps

**Step 1 —** Diagnostic step description.

**Step 2 —** Fix description.

---

## Issue 5 — [Error Message or Symptom]

**Severity:** High / Medium / Low

### Symptoms

- Symptom description

### Diagnostic Steps

**Step 1 —** Diagnostic step description.

**Step 2 —** Fix description.

---

## Collecting Diagnostic Information

When escalating an issue, collect the following before contacting support:

\`\`\`
Product: ${data.product_name || "Product Name"} ${data.version || ""}
Component: ${data.component || "Component"}
Error message: [exact text]
Steps to reproduce:
  1.
  2.
  3.
Browser/OS: [if applicable]
Screenshot: [attach if possible]
\`\`\`

---

## Escalation

If none of the steps in this guide resolve your issue:

**Contact:** ${data.support_email || "support@example.com"}
**Include:** The diagnostic information collected above
**SLA:** Response within 1 business day for Medium severity; 4 hours for High severity

---

## Related Documentation

- [Link to product documentation]
- [Link to API reference]
- [Link to changelog]
`;
    }
  }

};

// Export for use in app.js (or leave as global if not using modules)
// export default TEMPLATES;  // ← uncomment if using ES modules
