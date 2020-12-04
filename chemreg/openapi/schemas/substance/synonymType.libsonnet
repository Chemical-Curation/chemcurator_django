 {
  app: 'Substance',
  type: 'synonymType',
  description: 'A controlled vocabulary for recording and validating synonym types.',
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
    validationRegularExpression: {
      type: 'string',
      required: false,
    },
    scoreModifier: {
      type: 'number',
      format: 'float',
      default: '0',
    },
    isCasrn: {
      type: 'boolean',
    },
  },
}
