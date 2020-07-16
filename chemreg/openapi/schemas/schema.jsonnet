/////////////////////
// API description //
/////////////////////
local description = |||
  All about the chemreg API.

  ### OpenAPI
  This documentation is generated via the [OpenAPI specification](https://swagger.io/specification/) downloadable above. You can use this specification to assist in developing apps and using the API. For example, [Postman can import the OpenAPI specification](https://learning.postman.com/docs/postman/collections/working-with-openAPI/) to automatically build collections.

  ### JSON:API
  All endpoints follow the [JSON:API specification](https://jsonapi.org/).

  ### CORS
  This API features Cross-Origin Resource Sharing (CORS). Access to the API from browsers is restricted to a small number of domains.


  ### Authentication
  Two methods of authentication are available:
  - [HTTP basic authentication](https://en.wikipedia.org/wiki/Basic_access_authentication)
  - Session: A session will be made on the server after the first authenticated response. The response will include a cookie that sets the session ID. To mitigate CSRF attacks, the server uses the [strict SameSite policy](https://web.dev/samesite-cookies-explained/) in combination with the CORS policy detailed above.
|||;


///////////////////
// Import models //
///////////////////
// Compounds
local definedCompound = import 'compound/definedCompound.libsonnet';
local illDefinedCompound = import 'compound/illDefinedCompound.libsonnet';
local queryStructureType = import 'compound/queryStructureType.libsonnet';
local compound = import 'compound/compound.libsonnet';

// Substance
local synonymType = import 'substance/synonymType.libsonnet';
local source = import 'substance/source.libsonnet';

////////////////////////
// List of all models //
////////////////////////
local objs = [
  definedCompound,
  illDefinedCompound,
  queryStructureType,
  compound,
  synonymType,
  source
];

// Build spec
local jsonapi = import 'jsonapi.libsonnet';
jsonapi.buildSpec(objs, description)
