import fs from "node:fs/promises";
import path from "node:path";

const MARKER = "<!-- theme-coherence-check -->";

function readEnv(name) {
  const value = process.env[name];
  return typeof value === "string" ? value : "";
}

function requiredEnv(name) {
  const value = readEnv(name);
  if (!value) throw new Error(`Missing required env var: ${name}`);
  return value;
}

function safeJsonParse(text) {
  try {
    return JSON.parse(text);
  } catch {
    return undefined;
  }
}

function extractJsonObject(text) {
  const start = text.indexOf("{");
  const end = text.lastIndexOf("}");
  if (start === -1 || end === -1 || end <= start) return undefined;
  return safeJsonParse(text.slice(start, end + 1));
}

async function fileExists(filepath) {
  try {
    await fs.stat(filepath);
    return true;
  } catch {
    return false;
  }
}

function parseSkillFrontmatter(markdown) {
  const match = markdown.match(/^---\s*\n([\s\S]*?)\n---\s*\n/);
  if (!match) return { ok: false, error: "Missing YAML frontmatter block" };

  const frontmatter = match[1];
  const nameMatch = frontmatter.match(/^\s*name:\s*(.+)\s*$/m);
  const descriptionMatch = frontmatter.match(/^\s*description:\s*(.+)\s*$/m);

  const name = nameMatch?.[1]?.trim() ?? "";
  const description = descriptionMatch?.[1]?.trim() ?? "";

  if (!name) return { ok: false, error: "Frontmatter missing `name:`" };
  if (!description) return { ok: false, error: "Frontmatter missing `description:`" };

  return { ok: true, name, description };
}

async function githubRequest({ token, method, url, body }) {
  const response = await fetch(url, {
    method,
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "Content-Type": "application/json",
      "User-Agent": "theme-coherence-check",
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  const text = await response.text();
  const json = text ? safeJsonParse(text) : undefined;
  if (!response.ok) {
    const message =
      (typeof json === "object" && json && "message" in json && json.message) ||
      `${response.status} ${response.statusText}`;
    const error = new Error(`GitHub API error: ${message}`);
    error.status = response.status;
    error.url = url;
    error.body = json ?? text;
    throw error;
  }
  return json;
}

async function listPullRequestFiles({ token, owner, repo, pullNumber, maxFiles }) {
  const files = [];
  let page = 1;
  while (files.length < maxFiles) {
    const url = new URL(
      `https://api.github.com/repos/${owner}/${repo}/pulls/${pullNumber}/files`,
    );
    url.searchParams.set("per_page", "100");
    url.searchParams.set("page", String(page));

    const batch = await githubRequest({
      token,
      method: "GET",
      url: url.toString(),
    });

    if (!Array.isArray(batch) || batch.length === 0) break;
    for (const item of batch) files.push(item);
    if (batch.length < 100) break;
    page += 1;
  }

  return files.slice(0, maxFiles);
}

async function getRepoContentText({ token, owner, repo, ref, filepath }) {
  const encodedPath = filepath
    .split("/")
    .map((segment) => encodeURIComponent(segment))
    .join("/");
  const url = new URL(`https://api.github.com/repos/${owner}/${repo}/contents/${encodedPath}`);
  url.searchParams.set("ref", ref);

  const json = await githubRequest({ token, method: "GET", url: url.toString() });

  if (!json || typeof json !== "object") throw new Error(`Unexpected contents response for ${filepath}`);
  if (json.type !== "file") throw new Error(`Expected file content for ${filepath}`);
  if (typeof json.content !== "string") throw new Error(`Missing content for ${filepath}`);

  const raw = Buffer.from(json.content, "base64").toString("utf8");
  return raw;
}

async function upsertPrComment({ token, owner, repo, issueNumber, body }) {
  const listUrl = new URL(`https://api.github.com/repos/${owner}/${repo}/issues/${issueNumber}/comments`);
  listUrl.searchParams.set("per_page", "100");

  const comments = await githubRequest({ token, method: "GET", url: listUrl.toString() });
  const existing = Array.isArray(comments)
    ? comments.find(
        (c) =>
          c &&
          typeof c === "object" &&
          typeof c.body === "string" &&
          c.body.includes(MARKER) &&
          c.user &&
          typeof c.user === "object" &&
          c.user.login === "github-actions[bot]",
      )
    : undefined;

  if (existing && typeof existing.id === "number") {
    await githubRequest({
      token,
      method: "PATCH",
      url: `https://api.github.com/repos/${owner}/${repo}/issues/comments/${existing.id}`,
      body: { body },
    });
    return;
  }

  await githubRequest({
    token,
    method: "POST",
    url: `https://api.github.com/repos/${owner}/${repo}/issues/${issueNumber}/comments`,
    body: { body },
  });
}

function truncate(text, maxChars) {
  if (text.length <= maxChars) return text;
  return `${text.slice(0, maxChars)}\n\n[truncated to ${maxChars} chars]`;
}

async function callOpenAI({ apiKey, model, temperature, systemPrompt, userPrompt }) {
  const baseUrl = readEnv("OPENAI_BASE_URL") || "https://api.openai.com/v1";
  const url = `${baseUrl.replace(/\/$/, "")}/chat/completions`;

  const response = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model,
      temperature,
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt },
      ],
    }),
  });

  const text = await response.text();
  const json = text ? safeJsonParse(text) : undefined;
  if (!response.ok) {
    const message =
      (typeof json === "object" && json && "error" in json && json.error && json.error.message) ||
      `${response.status} ${response.statusText}`;
    const error = new Error(`OpenAI API error: ${message}`);
    error.status = response.status;
    error.body = json ?? text;
    throw error;
  }

  const content = json?.choices?.[0]?.message?.content;
  if (typeof content !== "string") throw new Error("OpenAI API returned no message content");
  const parsed = extractJsonObject(content);
  if (!parsed) {
    const error = new Error("Failed to parse JSON from OpenAI response");
    error.raw = content;
    throw error;
  }

  return parsed;
}

async function main() {
  const githubToken = requiredEnv("GITHUB_TOKEN");

  const eventPath = requiredEnv("GITHUB_EVENT_PATH");
  const event = safeJsonParse(await fs.readFile(eventPath, "utf8"));
  if (!event || typeof event !== "object") throw new Error("Failed to parse GitHub event payload");

  const pr = event.pull_request;
  if (!pr || typeof pr !== "object") {
    console.log("No pull_request in event payload; skipping.");
    return;
  }

  if (pr.draft) {
    console.log("Draft PR; skipping.");
    return;
  }

  const owner = event.repository?.owner?.login;
  const repo = event.repository?.name;
  if (!owner || !repo) throw new Error("Missing repository owner/name in event payload");

  const pullNumber = pr.number;
  if (typeof pullNumber !== "number") throw new Error("Missing pull_request.number");

  const configPath = path.join(process.cwd(), ".github", "theme-coherence.config.json");
  const themePath = path.join(process.cwd(), ".github", "theme-coherence.theme.md");
  const config = safeJsonParse(await fs.readFile(configPath, "utf8")) ?? {};
  const theme = await fs.readFile(themePath, "utf8");
  const requireOpenAI = config.requireOpenAI === true;
  const failOnOpenAIError = config.failOnOpenAIError === true;

  const skipLabels = Array.isArray(config.skipLabels) ? config.skipLabels : [];
  const prLabels = Array.isArray(pr.labels) ? pr.labels.map((l) => l?.name).filter(Boolean) : [];
  if (skipLabels.some((label) => prLabels.includes(label))) {
    console.log("Skip label present; skipping.");
    return;
  }

  const maxChangedFiles = typeof config.maxChangedFiles === "number" ? config.maxChangedFiles : 150;
  const maxDiffChars = typeof config.maxDiffChars === "number" ? config.maxDiffChars : 120000;
  const nonSkillDirs = Array.isArray(config.nonSkillDirs) ? config.nonSkillDirs : [];

  const files = await listPullRequestFiles({
    token: githubToken,
    owner,
    repo,
    pullNumber,
    maxFiles: maxChangedFiles,
  });

  const changedFiles = files.map((f) => ({
    filename: f.filename,
    status: f.status,
    patch: f.patch,
  }));

  const touchedTopDirs = new Set();
  for (const f of changedFiles) {
    if (!f.filename || typeof f.filename !== "string") continue;
    const [top] = f.filename.split("/");
    if (!top) continue;
    if (top.startsWith(".")) continue;
    if (nonSkillDirs.includes(top)) continue;
    if (f.filename.includes("/")) touchedTopDirs.add(top);
  }

  const headFullName = pr.head?.repo?.full_name;
  const headSha = pr.head?.sha;
  if (!headFullName || !headSha) throw new Error("Missing PR head repo/sha in event payload");
  const [headOwner, headRepo] = headFullName.split("/");

  const structuralIssues = [];

  for (const top of touchedTopDirs) {
    const localSkillPath = path.join(process.cwd(), top, "SKILL.md");
    const hasLocalSkill = await fileExists(localSkillPath);
    if (hasLocalSkill) continue;

    // New top-level directory (or one without SKILL.md in base): require SKILL.md in PR head.
    try {
      const headSkill = await getRepoContentText({
        token: githubToken,
        owner: headOwner,
        repo: headRepo,
        ref: headSha,
        filepath: `${top}/SKILL.md`,
      });
      const parsed = parseSkillFrontmatter(headSkill);
      if (!parsed.ok) {
        structuralIssues.push(
          `\`${top}/SKILL.md\` exists but is invalid: ${parsed.error}`,
        );
      }
    } catch (error) {
      if (error?.status === 404) {
        structuralIssues.push(
          `Top-level folder \`${top}/\` is touched but \`${top}/SKILL.md\` is missing.`,
        );
      } else {
        structuralIssues.push(
          `Failed to verify \`${top}/SKILL.md\`: ${error?.message ?? String(error)}`,
        );
      }
    }
  }

  const skillFilesToValidate = changedFiles
    .map((f) => f.filename)
    .filter((filename) => typeof filename === "string" && filename.endsWith("/SKILL.md"));

  const skillFrontmatterWarnings = [];
  for (const filename of skillFilesToValidate) {
    try {
      const content = await getRepoContentText({
        token: githubToken,
        owner: headOwner,
        repo: headRepo,
        ref: headSha,
        filepath: filename,
      });
      const parsed = parseSkillFrontmatter(content);
      if (!parsed.ok) {
        structuralIssues.push(`\`${filename}\` is invalid: ${parsed.error}`);
        continue;
      }

      const dir = filename.split("/")[0];
      if (dir && parsed.name !== dir) {
        skillFrontmatterWarnings.push(
          `\`${filename}\` frontmatter name is \`${parsed.name}\` but directory is \`${dir}\`.`,
        );
      }
    } catch (error) {
      structuralIssues.push(
        `Failed to read \`${filename}\` from PR head: ${error?.message ?? String(error)}`,
      );
    }
  }

  const skillInventory = [];
  for (const entry of await fs.readdir(process.cwd(), { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    if (entry.name.startsWith(".")) continue;
    if (nonSkillDirs.includes(entry.name)) continue;

    const skillPath = path.join(process.cwd(), entry.name, "SKILL.md");
    if (!(await fileExists(skillPath))) continue;
    const content = await fs.readFile(skillPath, "utf8");
    const parsed = parseSkillFrontmatter(content);
    if (!parsed.ok) continue;
    skillInventory.push({ dir: entry.name, name: parsed.name, description: parsed.description });
  }
  skillInventory.sort((a, b) => a.dir.localeCompare(b.dir));

  const prTitle = typeof pr.title === "string" ? pr.title : "";
  const prBody = typeof pr.body === "string" ? pr.body : "";

  let openaiResult;
  let openaiStatus = "skipped";
  const openaiApiKey = readEnv("OPENAI_API_KEY");
  if (openaiApiKey) {
    openaiStatus = "ok";
    const model = readEnv("OPENAI_MODEL") || config?.openai?.model || "gpt-4o-mini";
    const temperature =
      typeof config?.openai?.temperature === "number" ? config.openai.temperature : 0;

    const diffTextRaw = changedFiles
      .map((f) => {
        const header = `File: ${f.filename}\nStatus: ${f.status ?? "unknown"}`;
        const patch = typeof f.patch === "string" ? f.patch : "[patch unavailable]";
        return `${header}\n${patch}`;
      })
      .join("\n\n");

    const diffText = truncate(diffTextRaw, maxDiffChars);

    const systemPrompt = [
      "You are a reviewer for the-true-scotsman repository.",
      "Your job is to judge whether a PR's proposed changes are coherent with the project's theme and consistent in opinions across similar languages/frameworks.",
      "Be strict but fair. Prefer stable, cross-language principles and consistent terminology.",
      "Return ONLY valid JSON. No markdown, no prose.",
      "",
      "Theme rubric:",
      theme,
    ].join("\n");

    const userPrompt = [
      "Evaluate this pull request using the theme rubric.",
      "",
      `PR title: ${prTitle}`,
      prBody ? `PR body:\n${prBody}` : "PR body: (empty)",
      "",
      "Existing skills (base branch inventory):",
      ...skillInventory.map((s) => `- ${s.dir}: ${s.description}`),
      "",
      "Structural pre-check notes (from automation):",
      ...(structuralIssues.length
        ? structuralIssues.map((i) => `- ISSUE: ${i}`)
        : ["- No structural issues detected."]),
      ...(skillFrontmatterWarnings.length
        ? skillFrontmatterWarnings.map((w) => `- WARNING: ${w}`)
        : []),
      "",
      "Changed files diff (may be truncated; patches may be unavailable for large/binary files):",
      diffText,
      "",
      "Return JSON with this exact shape:",
      "{",
      '  "verdict": "pass" | "warn" | "fail",',
      '  "coherence_score": number,',
      '  "consistency_score": number,',
      '  "summary": string,',
      '  "reasons": string[],',
      '  "theme_violations": { "file": string, "details": string }[],',
      '  "consistency_issues": { "category": string, "details": string, "files": string[] }[],',
      '  "suggested_fixes": string[]',
      "}",
    ].join("\n");

    try {
      openaiResult = await callOpenAI({
        apiKey: openaiApiKey,
        model,
        temperature,
        systemPrompt,
        userPrompt,
      });
    } catch (error) {
      openaiStatus = "error";
      openaiResult = {
        verdict: "warn",
        summary: `OpenAI review failed: ${error?.message ?? String(error)}`,
        reasons: [],
        theme_violations: [],
        consistency_issues: [],
        suggested_fixes: ["Re-run after fixing OpenAI configuration (model/key/base URL)."],
      };
    }
  } else if (requireOpenAI) {
    openaiStatus = "missing_key";
    openaiResult = {
      verdict: "fail",
      summary: "LLM review is required but `OPENAI_API_KEY` is missing.",
      reasons: ["This workflow is configured to require an LLM-based theme/consistency review."],
      theme_violations: [],
      consistency_issues: [],
      suggested_fixes: [
        "Add `OPENAI_API_KEY` as a repository or organization secret.",
        "If you intentionally want to allow running without an LLM, set `requireOpenAI` to false in `.github/theme-coherence.config.json`.",
      ],
    };
  }

  const minCoherenceScore =
    typeof config.minCoherenceScore === "number" ? config.minCoherenceScore : 70;
  const minConsistencyScore =
    typeof config.minConsistencyScore === "number" ? config.minConsistencyScore : 70;

  let verdict = structuralIssues.length ? "fail" : "pass";

  if (openaiStatus === "ok" && openaiResult) {
    const coherence = Number(openaiResult.coherence_score);
    const consistency = Number(openaiResult.consistency_score);
    const modelVerdict =
      openaiResult.verdict === "fail" || openaiResult.verdict === "warn" ? openaiResult.verdict : "pass";

    if (verdict !== "fail") verdict = modelVerdict;
    if (verdict !== "fail" && (Number.isFinite(coherence) ? coherence : 0) < minCoherenceScore) {
      verdict = "fail";
    }
    if (verdict !== "fail" && (Number.isFinite(consistency) ? consistency : 0) < minConsistencyScore) {
      verdict = "fail";
    }
  } else if (verdict !== "fail" && openaiStatus !== "ok") {
    if (requireOpenAI) verdict = "fail";
    else if (openaiStatus === "error" && failOnOpenAIError) verdict = "fail";
    else verdict = "warn";
  } else if (skillFrontmatterWarnings.length) {
    verdict = "warn";
  }

  const shouldComment =
    (verdict === "pass" && config?.comment?.onPass) ||
    (verdict === "warn" && config?.comment?.onWarn) ||
    (verdict === "fail" && config?.comment?.onFail);

  const lines = [];
  lines.push(MARKER);
  lines.push(`## Theme coherence: ${verdict.toUpperCase()}`);
  lines.push("");
  lines.push(`- **PR**: #${pullNumber} — ${prTitle || "(no title)"}`);
  if (openaiStatus === "ok" && openaiResult) {
    lines.push(
      `- **Scores**: coherence ${openaiResult.coherence_score} / consistency ${openaiResult.consistency_score}`,
    );
  } else if (openaiStatus === "error" && openaiResult) {
    lines.push("- **LLM review**: error (see Summary)");
  } else if (openaiStatus === "missing_key") {
    lines.push("- **LLM review**: missing `OPENAI_API_KEY` (required)");
  } else {
    lines.push("- **LLM review**: skipped (missing `OPENAI_API_KEY`)");
  }
  lines.push(`- **Changed files**: ${changedFiles.length}`);
  lines.push("");

  if (structuralIssues.length) {
    lines.push("### Structural issues");
    for (const issue of structuralIssues) lines.push(`- ${issue}`);
    lines.push("");
  }

  if (skillFrontmatterWarnings.length) {
    lines.push("### Frontmatter warnings");
    for (const warn of skillFrontmatterWarnings) lines.push(`- ${warn}`);
    lines.push("");
  }

  if (openaiResult) {
    lines.push("### Summary");
    lines.push(openaiResult.summary || "(no summary)");
    lines.push("");

    const reasons = Array.isArray(openaiResult.reasons) ? openaiResult.reasons : [];
    if (reasons.length) {
      lines.push("### Reasons");
      for (const reason of reasons) lines.push(`- ${reason}`);
      lines.push("");
    }

    const themeViolations = Array.isArray(openaiResult.theme_violations)
      ? openaiResult.theme_violations
      : [];
    if (themeViolations.length) {
      lines.push("### Theme violations");
      for (const v of themeViolations) {
        if (!v || typeof v !== "object") continue;
        lines.push(`- \`${v.file ?? "?"}\`: ${v.details ?? ""}`.trim());
      }
      lines.push("");
    }

    const consistencyIssues = Array.isArray(openaiResult.consistency_issues)
      ? openaiResult.consistency_issues
      : [];
    if (consistencyIssues.length) {
      lines.push("### Consistency issues");
      for (const c of consistencyIssues) {
        if (!c || typeof c !== "object") continue;
        const filesList = Array.isArray(c.files) ? c.files.map((f) => `\`${f}\``).join(", ") : "";
        lines.push(
          `- **${c.category ?? "?"}**: ${c.details ?? ""}${filesList ? ` (${filesList})` : ""}`,
        );
      }
      lines.push("");
    }

    const fixes = Array.isArray(openaiResult.suggested_fixes) ? openaiResult.suggested_fixes : [];
    if (fixes.length) {
      lines.push("### Suggested fixes");
      for (const fix of fixes) lines.push(`- ${fix}`);
      lines.push("");
    }
  }

  const commentBody = lines.join("\n").trim() + "\n";

  if (shouldComment) {
    await upsertPrComment({
      token: githubToken,
      owner,
      repo,
      issueNumber: pullNumber,
      body: commentBody,
    });
  } else {
    console.log("Comment suppressed by config.");
  }

  if (verdict === "fail") {
    console.error("Theme coherence check failed.");
    process.exitCode = 1;
  } else if (verdict === "warn") {
    console.log("Theme coherence check warnings.");
  } else {
    console.log("Theme coherence check passed.");
  }
}

main().catch((error) => {
  console.error(error?.stack ?? String(error));
  process.exitCode = 1;
});
