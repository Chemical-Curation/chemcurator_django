local baseCompound = import 'baseCompound.libsonnet';
local queryStructureType = import 'queryStructureType.libsonnet';

{
  app: 'Compound',
  type: 'illDefinedCompound',
  description: 'Compounds that cannot be defined with molfiles.',
  attributes: {
    qcNote: baseCompound.attributes.qcNote,
    replacementCid: baseCompound.attributes.replacementCid,
    mrvfile: {
      type: 'string',
      description: 'The [ChemAxon MRV format](https://docs.chemaxon.com/display/docs/Marvin_Documents_-_MRV.html) representation for this compound.',
      example: '<?xml version="1.0" ?><cml><MDocument><MChemicalStruct><molecule><atomArray atomID="a1 a2" elementType="O O" x2="3.08 4.62" y2="0 0" /><bondArray><bond bondID="b1" atomRefs2="a1 a2" order="2"/></bondArray></molecule></MChemicalStruct></MDocument></cml>',
    },
  },
  relationships: [
    {
      object: queryStructureType,
      many: false,
      default: '1',
    },
  ],
  errors: [
    {
      status: 400,
      detail: 'The Query Structure Type submitted for this compound is no longer supported.',
      pointer: '/data/attributes/queryStructureType',
      code: 'invalid',
    },
  ],
}
