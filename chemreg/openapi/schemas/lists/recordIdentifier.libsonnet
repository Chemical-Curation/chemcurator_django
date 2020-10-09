local record = import 'record.libsonnet';
local identifier_type = import 'identifierType.libsonnet';
 
 {
  app: 'Lists',
  type: 'recordIdentifier',
  description: 'Everything about Record Identifiers.',
  attributes: {
    identifier: {
      type: 'string',
      maxLength: 50,
      required: true,
    },
    identifier_label: {
      type: 'string',
      maxLength: 100,
      required: true,
    },
  },
  relationships: [
    {
      object: record + 
        { 
          relationships: [] 
        },
      many: true,
      default: 1,
    },
    {
      object: identifier_type,
      many: false,
      default: 1,
    },
  ]
} 
