local definedCompound = import 'definedCompound.libsonnet';
local illDefinedCompound = import 'illDefinedCompound.libsonnet';

{
  app: 'Compound',
  type: 'compound',
  description: 'Aggregates all compounds.',
  readOnly: true,
  polymorphicObjects: [definedCompound, illDefinedCompound],
}
