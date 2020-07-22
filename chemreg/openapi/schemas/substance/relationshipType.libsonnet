 {
  app: 'Substance',
  type: 'relationshipType',
  description: 'Everything about Relationship Types.',
  attributes: {
    name: {
      type: 'string',
      maxLength: 49,
      pattern: '^[a-z0-9-]+$',
    },
    label: {
      type: 'string',
      maxLength: 99,
    },
    shortDescription: {
      type: 'string',
      maxLength: 499,
    },
    longDescription: {
      type: 'string',
    },
    corrolaryLabel: {
      type: 'string',
      maxLength: 99,
    },
    corrolaryShortDescription: {
      type: 'string',
      maxLength: 499,
    },
  },
}
