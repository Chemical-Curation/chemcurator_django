local list = import 'list.libsonnet';
local substance = import 'substance/substance.libsonnet';
 
 {
  app: 'Lists',
  type: 'record',
  description: 'Everything about Records.',
  attributes: {
    external_id: {
      type: 'string',
      maxLength: 500,
      required: true,
    },
    score: {
      type: 'float',
    },
    message: {
      type: 'string',
      maxLength: 500,
    },
    is_validated: {
      type: 'boolean',
    },
  },
  relationships: [
    {
      object: list + 
        { 
          relationships: [] 
        },
      many: false,
      default: 1,
    },
    {
      object: substance + 
        { 
          relationships: [] 
        },
      many: false,
      default: 1,
    },
    {
      object: {
        app: 'Lists',
        type: 'identifiers',
        description: 'Everything about Record Identifiers.',
        typePlural: 'identifers',
        hasRelationships: false,
        attributes: {
          none: {
            type: 'null',
          }
        },
      },
      many: true,
      required: false,
      default: 1,
    },
  ]
} 
