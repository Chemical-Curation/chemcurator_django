 {
  app: 'Substance',
  type: 'source',
  description: 'A controlled vocabulary for substance sources.',
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
  },
} 
