local baseCompound = import 'baseCompound.libsonnet';

{
  app: 'Compound',
  type: 'definedCompound',
  description: 'Everything about defined compounds.',
  queryParams: [
    {
      parameter: 'override',
      description: 'The computed InChIKey typically must be unique. However, in some circumstances, a non-unique InChIKey is allowed. An admin may add this query parameter in order to bypass uniqueness checks.',
    },
  ],
  attributes: {
    cid: baseCompound.attributes.cid,
    molfileV3000: {
      type: 'string',
      description: 'A [v3000 MDL Molfile](https://en.wikipedia.org/wiki/Chemical_table_file#The_Extended_Connection_Table_(V3000)) representing this compound. Newlines must be escaped (e.g. `\\n`) and spaces preserved.',
      example: '\n  -INDIGO-04212015202D\n\n  0  0  0  0  0  0  0  0  0  0  0 V3000\nM  V30 BEGIN CTAB\nM  V30 COUNTS 2 1 0 0 0\nM  V30 BEGIN ATOM\nM  V30 1 O 0.0 0.0 0.0 0\nM  V30 2 O 0.0 0.0 0.0 0\nM  V30 END ATOM\nM  V30 BEGIN BOND\nM  V30 1 2 1 2\nM  V30 END BOND\nM  V30 END CTAB\nM  END\n',
      oneOfGroup: 'structure',
    },
    smiles: {
      type: 'string',
      description: 'A [SMILES string](https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system) representing the compound.',
      example: 'O=O',
      writeOnly: true,
      oneOfGroup: 'structure',
    },
    molfileV2000: {
      type: 'any',
      description: 'A [v2000 MDL Molfile](https://en.wikipedia.org/wiki/Chemical_table_file#Molfile) representing the compound.',
      example: '\n  -INDIGO-04292017242D\n\n  2  1  0  0  0  0  0  0  0  0999 V2000\n    0.0000    0.0000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0\n    0.0000    0.0000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0\n  1  2  2  0  0  0  0\nM  END\n',
      writeOnly: true,
      oneOfGroup: 'structure',
    },
    inchikey: {
      type: 'string',
      maxLength: 29,
      readOnly: true,
      description: 'The computed [InChIKey](https://en.wikipedia.org/wiki/International_Chemical_Identifier#InChIKey) for this compound.',
      example: 'MYMOFIZGZYHOMD-UHFFFAOYSA-N',
    },
  },
  errors: [
    {
      status: 400,
      detail: 'Invalid format. Expected ' + std.extVar('COMPOUND_PREFIX') + 'CID$0######.',
      pointer: '/data/attributes/cid',
      code: 'invalid',
    },
    {
      status: 400,
      detail: 'Invalid checksum. Expected {real_checksum}.',
      pointer: '/data/attributes/cid',
      code: 'invalid',
    },
    {
      status: 400,
      detail: 'InChIKey not computable for provided structure.',
      pointer: '/data/attributes/{structureField}',
      code: 'invalid',
    },
    {
      status: 400,
      detail: 'InChIKey already exists.',
      pointer: '/data/attributes/{structureField}',
      code: 'invalid',
    },
    {
      status: 400,
      detail: 'Structure is not in SMILES format: {location of smiles error}',
      pointer: '/data/attributes/smiles',
      code: 'invalid',
    },
    {
      status: 400,
      detail: 'Cannot be converted into a molfile.',
      pointer: '/data/attributes/{structure}',
      code: 'invalid',
    },
    {
      status: 400,
      detail: 'Structure is not in V3000 format.',
      pointer: '/data/attributes/molfileV3000',
      code: 'invalid',
    },
    {
      status: 400,
      detail: 'Structure is not in V2000 format.',
      pointer: '/data/attributes/molfileV2000',
      code: 'invalid',
    },
    {
      status: 400,
      detail: "Only one of ['molfileV2000', 'molfileV3000', 'smiles'] allowed. Recieved {fields}.",
      pointer: '/data/attributes/nonFieldErrors',
      code: 'invalid',
    },
    {
      status: 400,
      detail: "One of ['molfileV2000', 'molfileV3000', 'smiles'] required.",
      pointer: '/data/attributes/nonFieldErrors',
      code: 'invalid',
    },
  ],
}
