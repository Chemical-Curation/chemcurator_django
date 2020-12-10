 {
  app: 'Substance',
  type: 'relationshipType',
  description: 'A controlled vocabulary to describe relationships among substances',
  attributes: {
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
    deprecated: {
      type: 'boolean',
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
