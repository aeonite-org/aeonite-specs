#!/usr/bin/env node

import { createHash } from 'node:crypto';
import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';

const repositoryRoot = path.resolve(import.meta.dirname, '..');
const sourceRoot = path.join(repositoryRoot, 'sources');
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

const files = await discover(sourceRoot, '.aeon');
const errors = [];
const ids = new Map();
const publicationPaths = new Map();

if (files.length !== 80) errors.push(`Expected 80 AEON specification sources, found ${files.length}.`);

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

process.stdout.write(`Checked ${files.length} canonical AEON sources and the v1 contract bundle.\n`);
