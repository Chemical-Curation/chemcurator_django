{
  attributes: {
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
