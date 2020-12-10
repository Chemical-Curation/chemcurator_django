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
local qcLevelsType = import 'substance/qcLevelsType.libsonnet';
local relationshipType = import 'substance/relationshipType.libsonnet';
local source = import 'substance/source.libsonnet';
local substance = import 'substance/substance.libsonnet';
local substanceRelationship = import 'substance/substanceRelationship.libsonnet';
local substanceType = import 'substance/substanceType.libsonnet';
local synonym = import 'substance/synonym.libsonnet';
local synonymQuality = import 'substance/synonymQuality.libsonnet';
local synonymType = import 'substance/synonymType.libsonnet';

// Lists
local externalContact = import 'lists/externalContact.libsonnet';
local list = import 'lists/list.libsonnet';
local listType = import 'lists/listType.libsonnet';
local accessibilityType = import 'lists/accessibilityType.libsonnet';
local identifierType = import 'lists/identifierType.libsonnet';
local record = import 'lists/record.libsonnet';
local recordIdentifier = import 'lists/recordIdentifier.libsonnet';

// Users
local user = import 'users/user.libsonnet';

////////////////////////
// List of all models //
////////////////////////
local objs = [
  // compounds
  definedCompound,
  illDefinedCompound,
  queryStructureType,
  compound,
  
  // substances
  qcLevelsType,
  relationshipType,
  source,
  substance,
  substanceRelationship,
  substanceType,
  synonym,
  synonymQuality,
  synonymType,

  //lists
  accessibilityType,
  list,
  listType,
  identifierType,
  record,
  recordIdentifier,
];

// Build spec
local jsonapi = import 'jsonapi.libsonnet';
jsonapi.buildSpec(objs, description)
