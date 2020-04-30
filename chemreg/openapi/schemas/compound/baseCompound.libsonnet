{
  attributes: {
    cid: {
      type: 'string',
      pattern: '^' + std.extVar('COMPOUND_PREFIX') + 'CID\\d0\\d+$',
      maxLength: 50,
      required: false,
      description: 'A unique identifier for this compound. It will be created if not provided.',
      example: std.extVar('COMPOUND_PREFIX') + 'CID702467346',
    },
  },
}
