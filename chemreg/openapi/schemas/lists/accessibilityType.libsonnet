{
  app: 'Lists',
  type: 'accessibilityType',
  description: 'A controlled vocabulary for Accessibility Types.',
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
