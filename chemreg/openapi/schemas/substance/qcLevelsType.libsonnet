 {
  app: 'Substance',
  type: 'qcLevel',
  description: 'A controlled vocabulary for describing QC levels',
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
    rank: {
      type: 'integer',
      example: 1,
    },
  },
}
