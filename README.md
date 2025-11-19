## All days have a separate .md files

# 📘 Full Training Report — Days 1 to 4

A complete consolidated documentation including **system setup, Node.js fundamentals, CLI application with concurrency, Git workflows, and API investigation**.

---

# **Day 1 — System Report & Node.js Fundamentals**

## 🖥️ 1. System Information

### OS Version

```bash
cat /etc/os-release
```

Output:

```
24.04.3
```

### Current Shell

```bash
echo $SHELL
```

Output:

```
/bin/bash
```

### Node Binary Path

```
/usr/bin/node
```

---

## ⚙️ 2. Install and Use NVM

Install:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
```

Load NVM:

```bash
export NVM_DIR="$HOME/.nvm"
```

Verify:

```bash
nvm -v
```

Install Node:

```bash
nvm install v24.11.0
nvm alias default v24.11.0
nvm use v24.11.0
```

---

## 🧩 3. `introspect.js`

```javascript
const os = require('os');

console.log('OS: ' + os.type());
console.log('Architecture: ' + os.arch());
console.log('CPU Cores: ' + os.cpus().length);
console.log('Total Memory: ' + os.totalmem());
console.log('System Uptime: ' + (os.uptime() / 3600).toFixed(2) + ' hours');
console.log('User: ' + os.userInfo().username);
console.log('Node Path: ' + process.execPath);
```

Run:

```bash
node introspect.js
```

---

## 📦 4. STREAM vs BUFFER Benchmark

Created 50MB file:

```bash
fallocate -l 50M testfile.txt
```

Or Node generator using `lorem-ipsum`.

Benchmark script compared:

* `fs.readFile` (Buffer)
* `fs.createReadStream` (Stream)

Results saved in:

```
logs/day1-perf.json
```

---

# **Day 2 — Node CLI App + Concurrency + Large Data Processing**

## 🎯 Objective

Build a **scalable CLI tool** for:

* Large text data analysis
* Concurrency
* Asynchronous I/O
* Performance benchmarking

---

## 📄 1. Generate Large Corpus File

`corpus.js`:

```js
const fs = require('fs');
const { loremIpsum } = require('lorem-ipsum');

const generateCorpus = () => {
  const numWords = 200000;
  let corpus = '';
  let w = 0;

  while (w < numWords) {
    corpus += loremIpsum({ count: 1000, units: 'words', format: 'plain' }) + ' ';
    w += 1000;
  }

  fs.writeFileSync('corpus.txt', corpus);
  console.log('Corpus generated:', w);
};

generateCorpus();
```

Run:

```bash
node corpus.js
```

---

## 🛠️ 2. CLI Tool — `wordstat.js`

Usage:

```bash
node wordstat.js --file corpus.txt --top 10 --minLen 5 --unique --concurrency 4
```

### CLI Options

| Option          | Alias | Description             |
| --------------- | ----- | ----------------------- |
| `--file`        | `-f`  | Path to text file       |
| `--top`         | `-t`  | Top N frequent words    |
| `--minLen`      | `-l`  | Minimum word length     |
| `--unique`      | `-u`  | Count only unique words |
| `--concurrency` | —     | Number of worker chunks |

---

## 📊 3. Output Files

### `output/stats.json`

```json
{
  "totalWords": 200000,
  "uniqueWords": 9998,
  "longestWord": "consectetur",
  "shortestWord": "ad",
  "topWords": [
    { "word": "lorem", "count": 1523 }
  ]
}
```

### `logs/perf-summary.json`

```json
[
  { "concurrency": 1, "duration": 5200 },
  { "concurrency": 4, "duration": 2300 },
  { "concurrency": 8, "duration": 1500 }
]
```

---

# **Day 3 — Git Workflows & Merge Post-Mortem**

## 📝 1. Repository With 8+ Commits

One commit intentionally included a bug (commit 4).

---

## 🔍 2. Locate Bug Using `git bisect`

```bash
git bisect start
git bisect bad
git bisect good <hash>
git bisect reset
```

Deliverable:

```
bisect-session.txt
```

---

## 🛠️ 3. Fix Bug & Revert Faulty Commit

```bash
git revert <faulty_commit_hash>
git commit -m "Fix bug introduced in commit 4"
```

---

## 📦 4. Git Stash Workflow

```bash
git stash
git pull
git stash apply
```

Deliverable:

```
stash-session.txt
```

---

## ⚔️ 5. Merge Conflicts (Two Clone Method)

```bash
git clone repo clone1
git clone repo clone2
```

Both clones edit the same line → commit → merge → conflict.

Conflict example:

```diff
<<<<<<< HEAD
Line from clone1
=======
Line from clone2
>>>>>>> branch
```

Resolved:

```
Line from clone1
Line from clone2
```

---

# **Day 4 — API Investigation & Networking Report**

## 🧰 Installed Tools

```bash
sudo apt install curl dnsutils traceroute nodejs npm -y
```

---

## 🌐 1. DNS Lookup

```bash
nslookup dummyjson.com
```

Findings:

* Cloudflare IPs (IPv4 & IPv6)
* Non-authoritative response

---

## 🌎 2. Traceroute

```bash
traceroute dummyjson.com
```

Displays all network hops.

---

## 🛰️ 3. CURL Requests (Pagination + Verbose)

```bash
curl -v "https://dummyjson.com/products?limit=5&skip=10"
```

Observations:

* DNS resolution
* TLS 1.3 handshake
* JSON response

---

## 🧪 4. Header Manipulation

### Remove User-Agent

```bash
curl -v -H "User-Agent:" https://dummyjson.com/products
```

### Fake Authorization

```bash
curl -v -H "Authorization: Bearer faketoken123"
```

DummyJSON ignores both for public endpoints.

---

## 🗂️ 5. ETag & Caching

### View headers

```bash
curl -I https://dummyjson.com/products/1
```

### Conditional GET

```bash
curl -v -H 'If-None-Match: <etag>' https://dummyjson.com/products/1
```

Response:

```
304 Not Modified
```

---

## ⚙️ 6. Node Server for Caching & Delay Simulation

`server.js`:

```javascript
const http = require('http');
const url = require('url');

const server = http.createServer((req, res) => {
  const { pathname, query } = url.parse(req.url, true);

  if (pathname === '/echo') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify(req.headers));
  }

  if (pathname === '/slow') {
    return setTimeout(() => {
      res.writeHead(200);
      res.end(`Delayed ${query.ms} ms`);
    }, parseInt(query.ms) || 1000);
  }

  if (pathname === '/cache') {
    res.writeHead(200, {
      'Cache-Control': 'max-age=30',
      'ETag': '"myetag123"'
    });
    return res.end('Cacheable response');
  }

  res.writeHead(404);
  res.end('Not found');
});

server.listen(3000, () => console.log('Server running on 3000'));
```

---

# 📦 Deliverables Summary

| Day       | Deliverables                                             |
| --------- | -------------------------------------------------------- |
| **Day 1** | `introspect.js`, stream vs buffer benchmarks             |
| **Day 2** | `corpus.js`, `wordstat.js`, stats/perf logs              |
| **Day 3** | `bisect-session.txt`, `stash-session.txt`, conflict file |
| **Day 4** | `curl-lab.txt`, `api-investigation.md`, `server.js`      |

---

# ✅ Summary

This README consolidates:

* System setup
* Node.js tooling
* Large file processing
* Concurrency + benchmarking
* Git debugging & merge workflows
* Curl, HTTP headers, caching, DNS
* Node HTTP server implementation

