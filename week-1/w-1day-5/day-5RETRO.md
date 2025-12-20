# Training Week 1 – Day 5

## Automated Build, Validation, and Git Hook Setup

This project demonstrates how to automate build validation, enforce code quality using Husky and ESLint, and schedule periodic builds using Cron in a Node.js environment.

---

## Project Overview

The setup ensures that:

* Code follows consistent linting and formatting rules.
* Configuration files are validated before every commit.
* Builds produce versioned artifacts with integrity checks.
* Automated builds run daily via a Cron job.

---

## Project Structure

```
Training-Week-1-Day-5/
├── artifacts/           # Stores build outputs (.tgz and .sha256)
├── logs/                # Stores cron logs
├── src/                 # Source code files
├── .husky/              # Git hooks (pre-commit validation)
├── build.sh             # Build automation script
├── validate.sh          # JSON validation script
├── .eslintrc.json       # ESLint configuration
├── .prettierrc          # Prettier configuration
├── package.json         # Node project metadata
└── README.md            # Documentation
```

---

## Setup Instructions

### 1. Initialize the Project

```bash
npm init -y
```
![alt text](<Screenshot from 2025-11-06 23-15-42.png>)

### 2. Install Required Tools

```bash
npm install eslint prettier husky jq
```
![alt text](<Screenshot from 2025-11-07 13-26-53.png>)


### 3. Configure ESLint & Prettier

Create `.eslintrc.json` and `.prettierrc` to enforce code consistency.

### 4. Add Validation Script

`validate.sh` checks if `config.json` is valid JSON:

![alt text](<Screenshot from 2025-11-07 13-28-23.png>)

```bash
#!/bin/bash
if jq empty config.json 2>/dev/null; then
  echo "Validation successful!"
else
  echo "ERROR: config.json is invalid JSON!"
  exit 1
fi
```



Make it executable:

```bash
chmod +x validate.sh
```

---

## Husky Pre-commit Hook

Initialize Husky:

```bash
npm pkg set scripts.prepare="husky"
npx husky init
```

Edit `.husky/pre-commit`:

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

./validate.sh
```

Then make it executable:

```bash
chmod +x .husky/pre-commit
```
![alt text](<Screenshot from 2025-11-07 16-45-00.png>)

 **Now, commits will be blocked** if validation fails.

![alt text](<Screenshot from 2025-11-07 16-47-33.png>)

---

## Build Script

`build.sh` creates a versioned `.tgz` archive and a `.sha256` checksum file inside `/artifacts`:

```bash
#!/bin/bash
timestamp=$(date +%Y%m%d-%H%M%S)
tar czf artifacts/build-$timestamp.tgz src
sha256sum artifacts/build-$timestamp.tgz > artifacts/build-$timestamp.sha256
echo " Build successful: build-$timestamp.tgz"
```

Make it executable:

```bash
chmod +x build.sh
```

Run manually:

```bash
./build.sh
```
![alt text](<Screenshot from 2025-11-07 14-32-54.png>)
---

## Cron Job Automation

Schedule automatic builds:

```bash
crontab -e
```

Add this line to run every day at 2:55 PM:

```
55 14 * * * /home/username/Training-Week-1-Day-5/build.sh >> /home/username/Training-Week-1-Day-5/logs/cron.log 2>&1
```

Check your scheduled tasks:

```bash
crontab -l
```

---

## Validation Flow

1. You modify your code.
2. On `git commit`, Husky runs `validate.sh`.
3. If the JSON is valid → commit succeeds.
4. If not → commit fails with an error message.

---

## Build Artifacts

Each successful build generates:

* `build-<timestamp>.tgz` → Compressed build file
* `build-<timestamp>.sha256` → Integrity verification file

Artifacts are stored inside `/artifacts`.

---

## Key Learnings

* Automating validation and build improves consistency.
* Husky hooks enforce standards before code reaches the repository.
* Cron jobs ensure regular builds without manual effort.
* `jq`, ESLint, and Prettier together maintain project hygiene.

---