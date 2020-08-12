 {
  app: 'Users',
  type: 'user',
  description: 'System user accounts.',
  attributes: {
    username: {
      type: 'string',
      maxLength: 150,
      required: true,
    },
    first_name: {
      type: 'string',
      maxLength: 30,
    },
    last_name: {
      type: 'string',
      maxLength: 150,
    },
    email: {
      type: 'string',
    },
    is_superuser: {
      type: 'boolean',
    },
  },
}            
