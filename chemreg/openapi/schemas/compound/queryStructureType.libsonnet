{
  app: 'Compound',
  type: 'queryStructureType',
  description: 'Query structure types will persist on DELETE and will be flagged as `"deprecated"` disabling them from being related to an illDefinedCompound.',
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
      readOnly: true,
    },
  },
}
