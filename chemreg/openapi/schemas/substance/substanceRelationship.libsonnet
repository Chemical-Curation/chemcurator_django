local source = import 'source.libsonnet';
local relationship_type = import 'relationshipType.libsonnet';
local substance = import 'substance.libsonnet';
local from_substance = substance;
local to_substance = substance;


 {
  app: 'Substance',
  type: 'substanceRelationship',
  description: 'Everything about Substance Relationships.',
  attributes: {
    qc_notes: {
      type: 'string',
    },
  },
  relationships: [
    {
        object: substance + 
        { 
          relationships: [], 
          type: 'fromSubstance'
        },
        many: false,
        default: 1,
    },
    {
        object: substance + 
        { 
          relationships: [], 
          type: 'toSubstance'
        },
        many: false,
        default: 1,
    },
    {
      object: source,
      many: false,
      default: 1,
    },
    {
      object: relationship_type,
      many: false,
      default: 1,
    },
  ]
}
