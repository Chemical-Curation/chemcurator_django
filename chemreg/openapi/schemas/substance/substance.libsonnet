local source = import 'source.libsonnet';
local substance_type = import 'substanceType.libsonnet';
local qc_level = import 'qcLevelsType.libsonnet';

 {
  app: 'Substance',
  type: 'substance',
  description: 'Substances.',
  attributes: {
    preferred_name: {
      type: 'slug',
      maxLength: 255,
      pattern: '^[a-z0-9-]+$',
      required: true,
    },
    display_name: {
      type: 'string',
      maxLength: 255,
      required: true,
    },
    description: {
      type: 'string',
      maxLength: 1024,
    },
    public_qc_note: {
      type: 'string',
      maxLength: 1024,
    },
    private_qc_note: {
      type: 'string',
      maxLength: 1024,
    },
    casrn: {
      type: 'string',
      unique: true,
    },
  },
  relationships: [
    {
      object: source,
      many: false,
      default: 1,
    },
    {
      object: substance_type,
      many: false,
      default: 1,
    },
    {
      object: qc_level,
      many: false,
      default: 1,
    },
    {
      object: {
        app: 'Compound',
        type: 'associatedCompound',
        description: 'Polymorphic related resource receiving either defined or ill-defined compounds.',
        typePlural: 'associatedCompounds',
        hasRelationships: false,
        attributes: {
          none: {
            type: 'null',
          }
        },
      },
      many: false,
      required: false,
      default: 1,
    },
  ]
}
