 {
  app: 'Substance',
  type: 'synonymQuality',
  typePlural: 'synonymQualities',
  description: 'Everything about Synonym Qualities.',
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