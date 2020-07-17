 {
  app: 'Substance',
  type: 'qcLevel',
  description: 'Everything about Sources.',
  attributes: {
    name: {
      type: 'slug',
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
    rank: {
      type: 'integer',
      example: 1,
    },
  },
}
