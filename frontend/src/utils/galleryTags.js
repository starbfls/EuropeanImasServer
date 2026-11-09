// New photos have a types array; older photos retain their single type field.
export function photoTagIds(photo) {
  const values = Array.isArray(photo.types) && photo.types.length ? photo.types : [photo.type]
  return [...new Set(values.filter(value => typeof value === 'string' && value.trim()).map(value => value.trim()))]
}

export function photoTagLabels(photo) {
  const ids = photoTagIds(photo)
  const labels = Array.isArray(photo.type_labels) ? photo.type_labels : []
  return ids.map((id, index) => labels[index] || (ids.length === 1 && photo.type_label) || id)
}

export function toggleTag(selected, id) {
  return selected.includes(id) ? selected.filter(value => value !== id) : [...selected, id]
}

export function matchesPhotoTags(photo, selected) {
  const ids = photoTagIds(photo)
  return selected.every(id => ids.includes(id))
}
