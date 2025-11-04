In FBA, we have extensively customized the Schema. For details, please refer to the source code: `backend\common\schema.py`

## Class Naming

Follow these naming conventions:

- Base schema: `XxxSchemaBase(SchemaBase)`
- Interface input parameters: `XxxParam()`
- New input parameters: `CreateXxxParam()`
- Update parameters: `UpdateXxxParam()`
- Batch delete parameters: `DeleteXxxParam()`
- Query details: `GetXxxDetail()`
- Query details (including relationships): `GetXxxWithRelationDetail()`
- Query tree: `GetXxxTree()`

## Field Definitions

- Avoid setting required fields to `...` as default values. See: [Required Fields](https://docs.pydantic.dev/latest/concepts/models/#required-fields)
- Add `description` parameters to all fields for improved API documentation

## CamelCase Response

[Please refer to **API Responses**](response.md#camelCase_Returns){.read-more}
