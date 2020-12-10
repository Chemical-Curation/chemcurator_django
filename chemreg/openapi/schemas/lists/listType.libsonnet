 {
  app: 'Lists',
  type: 'listType',
  description: 'A controlled vocabulary for List Types.',
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
