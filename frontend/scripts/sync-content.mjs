// Generate public fallback data from the same content used by the Flask API.
// Never read local submissions, uploads, or environment files here.
import { mkdir, readFile, writeFile } from 'node:fs/promises'

const source = new URL('../../backend/data/content/', import.meta.url)
const target = new URL('../src/data/generated/', import.meta.url)
const files = ['announcements.json', 'imas_events.json']
const generated = await Promise.all(files.map(async (name) => {
  const rows = JSON.parse(await readFile(new URL(name, source), 'utf8'))
  if (!Array.isArray(rows)) throw new Error(`${name}: expected an array`)
  return [name, `${JSON.stringify(rows, null, 2)}\n`]
}))

await mkdir(target, { recursive: true })
for (const [name, content] of generated) {
  const path = new URL(name, target)
  let previous
  try {
    previous = await readFile(path, 'utf8')
  } catch (error) {
    if (error.code !== 'ENOENT') throw error
  }
  if (previous !== content) await writeFile(path, content, 'utf8')
}
console.log('Public event fallback data synchronized.')
