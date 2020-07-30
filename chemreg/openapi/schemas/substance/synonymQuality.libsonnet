 {
  app: 'Substance',
  type: 'synonymQuality',
  typePlural: 'synonymQualities',
  description: 'A controlled vocabulary for recording synonym quality.',
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
    deprecated: {
      type: 'boolean',
    },
    scoreWeight: {
      type: 'number',
      format: 'float',
      default: '1.0',
    },
    isRestrictive: {
      type: 'boolean',
      default: 'false',
    },
  },
} 