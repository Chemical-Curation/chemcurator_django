 {
  app: 'Lists',
  type: 'identifierType',
  description: 'A controlled vocabulary for describing the identified control type that controls the identifier.',
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
