import test from 'node:test'
import assert from 'node:assert/strict'
import { matchesPhotoTags, photoTagIds, photoTagLabels, toggleTag } from '../src/utils/galleryTags.js'

test('old single-tag photos remain searchable and keep their label', () => {
  const photo = { type: 'doll', type_label: '娃娃' }
  assert.deepEqual(photoTagIds(photo), ['doll'])
  assert.deepEqual(photoTagLabels(photo), ['娃娃'])
  assert(matchesPhotoTags(photo, ['doll']))
  assert(!matchesPhotoTags(photo, ['doll', 'mochi']))
})

test('array tags take precedence over the legacy primary tag', () => {
  const photo = { type: 'doll', types: ['mochi', ' nunu ', 'mochi', '', null] }
  assert.deepEqual(photoTagIds(photo), ['mochi', 'nunu'])
  assert.deepEqual(photoTagIds({ types: [], type: 'doll' }), ['doll'])
  assert.deepEqual(photoTagIds({}), [])
})

test('clicking a selected tag cancels it without clearing other selections', () => {
  const initial = ['gkmas_shirube_final']
  const selected = toggleTag(initial, 'mochi')
  assert.deepEqual(initial, ['gkmas_shirube_final'])
  assert.deepEqual(selected, ['gkmas_shirube_final', 'mochi'])
  assert.deepEqual(toggleTag(selected, 'mochi'), initial)
  assert.deepEqual(toggleTag(initial, 'gkmas_shirube_final'), [])
})

test('multiple gallery filters require every selected tag and clear to all photos', () => {
  const photo = { types: ['gkmas_shirube_final', 'mochi'], type_labels: ['学园现地', 'mochi'] }
  assert(matchesPhotoTags(photo, []))
  assert(matchesPhotoTags(photo, ['mochi']))
  assert(matchesPhotoTags(photo, ['gkmas_shirube_final', 'mochi']))
  assert(!matchesPhotoTags(photo, ['gkmas_shirube_final', 'nunu']))
  assert.deepEqual(photoTagLabels(photo), ['学园现地', 'mochi'])
})
