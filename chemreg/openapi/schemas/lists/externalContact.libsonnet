 {
  app: 'Lists',
  type: 'externalContact',
  description: 'Contact information for individuals and organizations associated with a List',
  attributes: {
    name: {
      type: 'string',
      maxLength: 49,
      required: true,
    },
    email: {
      type: 'string',
      maxLength: 49,
      required: true,
    },
    phone: {
      type: 'string',
      maxLength: 15,
      required: true,
    },
  },
} 