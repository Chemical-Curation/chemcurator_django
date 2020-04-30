local baseCompound = import 'baseCompound.libsonnet';

{
  app: 'Compound',
  type: 'definedCompound',
  description: 'Everything about defined compounds.',
  attributes: {
    cid: baseCompound.attributes.cid,
    molfileV3000: {
      type: 'string',
      description: 'A [v3000 MDL Molfile](https://en.wikipedia.org/wiki/Chemical_table_file#The_Extended_Connection_Table_(V3000)) representing this compound. Newlines must be escaped (e.g. \\n) and spaces preserved.',
      example: '\\n  -CHEMREG-04212015202D\\n\\n  0  0  0  0  0  0  0  0  0  0  0 V3000\\nM  V30 BEGIN CTAB\\nM  V30 COUNTS 2 1 0 0 0\\nM  V30 BEGIN ATOM\\nM  V30 1 O 0.0 0.0 0.0 0\\nM  V30 2 O 0.0 0.0 0.0 0\\nM  V30 END ATOM\\nM  V30 BEGIN BOND\\nM  V30 1 2 1 2\\nM  V30 END BOND\\nM  V30 END CTAB\\nM  END\\n',
      oneOfGroup: 'structure',
    },
    smiles: {
      type: 'any',
      description: 'A [SMILES string](https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system) representing the compound.',
      example: 'O=O',
      writeOnly: true,
      oneOfGroup: 'structure',
    },
    molfileV2000: {
      type: 'any',
      description: 'A [v2000 MDL Molfile](https://en.wikipedia.org/wiki/Chemical_table_file#Molfile) representing the compound.',
      example: '\\n  -CHEMREG-04292017242D\\n\\n  2  1  0  0  0  0  0  0  0  0999 V2000\\n    0.0000    0.0000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0\\n    0.0000    0.0000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0\\n  1  2  2  0  0  0  0\\nM  END\\n',
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
    override: {
      type: 'any',
      required: false,
      writeOnly: true,
      description: 'The computed InChIKey typically must be unique. However, in some circumstances, a non-unique InChIKey is allowed. Any logged in user may set this to `true` (or any other "truthy" value) in order to bypass uniqueness checks.',
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
      pointer: '/data/attributes/inchikey',
      code: 'invalid',
    },
    {
      status: 400,
      detail: 'InChIKey already exists.',
      pointer: '/data/attributes/molfileV3000',
      code: 'invalid',
    },
    {
      status: 400,
      detail: 'The SMILES string cannot be converted to a molfile.\n {location of smiles error}',
      pointer: '/data/attributes/smiles',
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
      detail: 'Molfile format is invalid. Molfile v2000 format expected.',
      pointer: '/data/attributes/molfileV3000',
      code: 'invalid',
    },
    {
      status: 400,
      detail: 'The data includes too many potential non-V3000 molfile structures in {matched}.',
      pointer: '/data/attributes/molfileV3000',
      code: 'invalid',
    },
  ],
}
