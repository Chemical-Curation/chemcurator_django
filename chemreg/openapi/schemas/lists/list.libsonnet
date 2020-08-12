local list_accessibility = import 'accessibilityType.libsonnet';
local external_contact = import 'externalContact.libsonnet';
local types = import 'listType.libsonnet';
local owners = import 'users/user.libsonnet';
 
 {
  app: 'Lists',
  type: 'list',
  description: 'Lists of chemicals with associated metadata.',
  attributes: {
    name: {
      type: 'string',
      maxLength: 50,
      pattern: '^[a-z0-9-]+$',
      required: true,
    },
    label: {
      type: 'string',
      maxLength: 255,
      required: true,
    },
    shortDescription: {
      type: 'string',
      maxLength: 1000,
      required: true,
    },
    longDescription: {
      type: 'string',
      required: true,
    },
    source_url: {
      type: 'string',
      maxLength: 500,
    },
    source_reference: {
      type: 'string',
      maxLength: 500,
    },
    source_doi: {
      type: 'string',
      maxLength: 500,
    },
    date_of_source_collection: {
      type: 'date',
      required: true,
    },
  },
  relationships: [
    {
      object: list_accessibility,
      many: false,
      default: 1,
    },
    {
      object: external_contact,
      many: false,
      default: 1,
    },
    {
      object: types,
      many: true,
      default: 1,
    },
    {
      object: owners,
      many: true,
      default: 'current_user',
    },
  ]
} 