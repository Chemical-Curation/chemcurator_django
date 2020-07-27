local source = import 'source.libsonnet';
local substance = import 'substance.libsonnet';
local synonym_quality = import 'synonymQuality.libsonnet';
local synonym_type = import 'synonymType.libsonnet';

 {
  app: 'Substance',
  type: 'synonym',
  description: 'Everything about Synonyms.',
  attributes: {
    identifier: {
      type: 'string',
      maxLength: 1024,
    },
    qc_notes: {
      type: 'string',
      maxLength: 1024,
      required: false,
    },
  },
  relationships: [
    {
      object: source,
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
      object: synonym_quality,
      many: false,
      default: 1,
    },
    {
      object: synonym_type,
      many: false,
      required: false,
      default: 1,
    },
  ]
}
