{
  attributes: {
    cid: {
      type: 'string',
      pattern: '^' + std.extVar('COMPOUND_PREFIX') + 'CID\\d0\\d+$',
      maxLength: 50,
      required: false,
      description: 'A unique identifier for this compound. It will be created if not provided. \n        \n If included in the body of a request, admin permissions are required.',
      example: std.extVar('COMPOUND_PREFIX') + 'CID702467346',
      filter: true,
    },
    qcNote: {
      type: 'string',
      description: 'A note explaining why a compound was deleted in favor of a different record.',
      delete: true,
    },
    replacementCid: {
      type: 'string',
      description: 'The CID of the compound replacing this one.',
      delete: true,
    },
  },
}
