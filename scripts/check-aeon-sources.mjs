#!/usr/bin/env node

import { createHash } from 'node:crypto';
import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';

const repositoryRoot = path.resolve(import.meta.dirname, '..');
const sourceRoot = path.join(repositoryRoot, 'sources');
const publicationResourceRoot = path.join(repositoryRoot, 'resources');
const resourceRoot = path.join(repositoryRoot, 'resources/contracts/v1');
const requiredFields = [
  ['schemaVersion', 'string'],
  ['id', 'string'],
  ['title', 'string'],
  ['description', 'string'],
  ['created', 'date'],
  ['modified', 'date'],
  ['family', 'string'],
  ['group', 'string'],
  ['standing', 'string'],
  ['lifecycle', 'string'],
  ['normativity', 'string'],
  ['license', 'string'],
  ['path', 'string'],
  ['order', 'number'],
  ['publish', 'boolean'],
  ['keywords', 'list<string>'],
  ['related', 'list<string>'],
  ['bodyFormat', 'string'],
];

async function discover(directory, extension) {
  const files = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await discover(target, extension));
    if (entry.isFile() && entry.name.endsWith(extension)) files.push(target);
  }
  return files.sort();
}

function declaration(source, name, type) {
  const escapedType = type.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return new RegExp(`^${name}:${escapedType}\\s*=\\s*(.+)$`, 'm').exec(source)?.[1]?.trim();
}

function stringValue(value) {
  const match = /^"([\s\S]*)"$/.exec(value ?? '');
  return match?.[1];
}

function stringListValue(value) {
  try {
    const parsed = JSON.parse(value ?? '');
    return Array.isArray(parsed) && parsed.every((entry) => typeof entry === 'string') ? parsed : null;
  } catch {
    return null;
  }
}

function isEscaped(value, index) {
  let backslashes = 0;
  for (let cursor = index - 1; cursor >= 0 && value[cursor] === '\\'; cursor -= 1) backslashes += 1;
  return backslashes % 2 === 1;
}

function findUnescaped(value, character, fromIndex) {
  for (let index = fromIndex; index < value.length; index += 1) {
    if (value[index] === character && !isEscaped(value, index)) return index;
  }
  return -1;
}

function proseBody(source) {
  return /^body:prose\s*=\s*>`\s*\n([\s\S]*)\n`\s*$/m.exec(source)?.[1] ?? '';
}

function publicationReferences(source) {
  const anchors = [];
  const links = [];
  let rawBlock = null;

  for (const line of proseBody(source).split(/\r?\n/)) {
    const markerLine = line.trimStart().replaceAll('\\`', '`');
    if (rawBlock !== null) {
      const closes = rawBlock === 'backtick'
        ? markerLine.startsWith('```')
        : rawBlock === 'dollar'
          ? markerLine.startsWith('~~~$')
          : /^\+\+\+(?:\s+\(.*\))?\s*$/.test(markerLine);
      if (closes) rawBlock = null;
      continue;
    }
    if (markerLine.startsWith('```')) {
      rawBlock = 'backtick';
      continue;
    }
    if (markerLine.startsWith('~~~$')) {
      rawBlock = 'dollar';
      continue;
    }
    if (/^\+\+\+[A-Za-z]/.test(markerLine)) {
      rawBlock = 'extension';
      continue;
    }

    for (let index = 0; index < line.length - 1; index += 1) {
      if (line[index] !== '[' || isEscaped(line, index)) continue;
      const kind = line[index + 1];
      if (kind === '$') {
        for (let end = index + 2; end < line.length; end += 1) {
          if (line[end] === ']' && line[end - 1] !== '\\') {
            index = end;
            break;
          }
        }
      } else if (kind === '#') {
        const end = findUnescaped(line, ']', index + 2);
        if (end !== -1) {
          anchors.push(line.slice(index + 2, end).trim());
          index = end;
        }
      } else if (kind === '@') {
        const separator = findUnescaped(line, '|', index + 2);
        if (separator !== -1) links.push(line.slice(index + 2, separator).trim());
      }
    }
  }

  return { anchors, links };
}

const files = await discover(sourceRoot, '.aeon');
const errors = [];
const ids = new Map();
const publicationPaths = new Map();
const documents = [];

if (files.length !== 87) errors.push(`Expected 87 AEON specification sources, found ${files.length}.`);

for (const file of files) {
  const relative = path.relative(repositoryRoot, file).split(path.sep).join('/');
  const source = await readFile(file, 'utf8');
  for (const [name, type] of requiredFields) {
    if (declaration(source, name, type) === undefined) errors.push(`${relative}: missing ${name}:${type}.`);
  }
  if (!/^body:prose\s*=\s*>`\s*$/m.test(source) || !/`\s*$/.test(source)) {
    errors.push(`${relative}: missing a complete body:prose trimtick.`);
  }

  const id = stringValue(declaration(source, 'id', 'string'));
  const publicationPath = stringValue(declaration(source, 'path', 'string'));
  const created = declaration(source, 'created', 'date');
  const modified = declaration(source, 'modified', 'date');
  const bodyFormat = stringValue(declaration(source, 'bodyFormat', 'string'));
  const publish = declaration(source, 'publish', 'boolean') === 'true';
  const related = stringListValue(declaration(source, 'related', 'list<string>'));

  if (!id || !/^[a-z][a-z0-9-]*$/.test(id)) errors.push(`${relative}: invalid document id.`);
  if (id && ids.has(id)) errors.push(`${relative}: duplicate id also used by ${ids.get(id)}.`);
  if (id) ids.set(id, relative);
  if (!publicationPath || publicationPath.startsWith('/') || publicationPath.includes('..')) {
    errors.push(`${relative}: invalid publication path.`);
  }
  if (publicationPath && publicationPaths.has(publicationPath)) {
    errors.push(`${relative}: duplicate publication path also used by ${publicationPaths.get(publicationPath)}.`);
  }
  if (publicationPath) publicationPaths.set(publicationPath, relative);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(created ?? '') || !/^\d{4}-\d{2}-\d{2}$/.test(modified ?? '')) {
    errors.push(`${relative}: created and modified must be ISO dates.`);
  } else if (created > modified) {
    errors.push(`${relative}: created date is later than modified date.`);
  }
  if (!['and-v1', 'and-v2'].includes(bodyFormat ?? '')) {
    errors.push(`${relative}: unsupported bodyFormat ${bodyFormat ?? '<missing>'}.`);
  }
  if (related === null) errors.push(`${relative}: related must be a list of document IDs.`);
  documents.push({ relative, id, publish, related: related ?? [], ...publicationReferences(source) });
}

const assetPaths = new Set(
  (await discover(publicationResourceRoot, '')).map(
    (file) => `assets/${path.relative(publicationResourceRoot, file).split(path.sep).join('/')}`,
  ),
);
let checkedLinks = 0;
for (const document of documents) {
  const anchorSet = new Set();
  for (const anchor of document.anchors) {
    if (!/^[A-Za-z0-9][A-Za-z0-9._:-]*$/.test(anchor)) {
      errors.push(`${document.relative}: invalid anchor ${anchor || '<empty>'}.`);
    } else if (anchorSet.has(anchor)) {
      errors.push(`${document.relative}: duplicate anchor ${anchor}.`);
    }
    anchorSet.add(anchor);
  }
  document.anchorSet = anchorSet;

  for (const relatedId of document.related) {
    if (!ids.has(relatedId)) errors.push(`${document.relative}: related document ${relatedId} does not exist.`);
  }
}

const documentTarget = /^document:([A-Za-z][A-Za-z0-9._:-]*)(?:#([A-Za-z0-9][A-Za-z0-9._:-]*))?$/;
for (const document of documents) {
  for (const target of document.links) {
    checkedLinks += 1;
    if (target.startsWith('document:')) {
      const match = documentTarget.exec(target);
      if (!match) {
        errors.push(`${document.relative}: malformed publication document target ${target}.`);
        continue;
      }
      const destination = documents.find((candidate) => candidate.id === match[1]);
      if (!destination || !destination.publish) {
        errors.push(`${document.relative}: publication document target ${match[1]} is missing or unpublished.`);
      } else if (match[2] && !destination.anchorSet.has(match[2])) {
        errors.push(`${document.relative}: publication document anchor ${match[1]}#${match[2]} does not exist.`);
      }
      continue;
    }
    if (target.startsWith('#')) {
      const anchor = target.slice(1);
      if (!document.anchorSet.has(anchor)) errors.push(`${document.relative}: local anchor ${target} does not exist.`);
      continue;
    }
    if (/^(?:\.{1,2}\/)+.*\.md(?:#.*)?$/.test(target)) {
      errors.push(`${document.relative}: relative Markdown target ${target} is not portable; use document:<id>.`);
      continue;
    }
    if (target.startsWith('../assets/') || target.startsWith('/artifacts/assets/')) {
      const artifact = target.startsWith('/artifacts/assets/')
        ? `assets/${target.slice('/artifacts/assets/'.length)}`
        : path.posix.normalize(path.posix.join('html', target)).replace(/^\.\//, '');
      if (!assetPaths.has(artifact)) errors.push(`${document.relative}: publication asset ${target} does not exist.`);
    }
  }
}

const registry = JSON.parse(await readFile(path.join(resourceRoot, 'registry.json'), 'utf8'));
for (const entry of registry.contracts ?? []) {
  const artifactPath = path.join(resourceRoot, entry.path);
  const artifact = await readFile(artifactPath);
  const digest = createHash('sha256').update(artifact).digest('hex');
  if (digest !== entry.sha256) errors.push(`resources/contracts/v1/${entry.path}: registry hash mismatch.`);
}

if (errors.length > 0) {
  process.stderr.write(`${errors.join('\n')}\n`);
  process.exit(1);
}

process.stdout.write(`Checked ${files.length} canonical AEON sources, ${checkedLinks} publication links, and the v1 contract bundle.\n`);
