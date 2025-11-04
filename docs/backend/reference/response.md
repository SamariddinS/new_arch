---
title: API Response
---

We have developed a very flexible and comprehensive API response system for fba that is also suitable for any FastAPI application.

## Unified Response Model

In typical web application development, the response structure is usually unified. However, FastAPI's official tutorial doesn't show how to do this. Actually, it's quite simple—
just provide a unified pydantic model.

```python
class ResponseModel(BaseModel):
    code: int = CustomResponseCode.HTTP_200.code
    msg: str = CustomResponseCode.HTTP_200.msg
    data: Any | None = None
```

Below is an example of using this model for returns (following FastAPI official tutorial). You can choose either the `response_model` parameter or the `->` type—FastAPI
will automatically parse and obtain the final response structure internally.

`response_model` parameter:

```python{1,3}
@router.get('/test', response_model=ResponseModel)
def test():
    return ResponseModel(data={'test': 'test'})
```

`->` type:

```python{2,3}
@router.get('/test')
def test() -> ResponseModel:
    return ResponseModel(data={'test': 'test'})
```

## Schema Mode

We've explained the unified response model above. However, one of FastAPI's advantages is fully automatic OpenAPI and documentation. If we globally use
ResponseModel as the unified response model, you'll get this in the Swagger docs (as shown):

![response_model](/images/response_model.png)

Obviously, we cannot get the data structure in the response. At this point, your frontend colleague finds you. Will you tell them, "Just make a request and you'll see"? (That's fine, but clearly not very friendly). Below is the unified response model we created for
Schema mode:

```python
class ResponseSchemaModel(ResponseModel, Generic[SchemaT]):
    data: SchemaT
```

Below is an example of using this model for returns (following FastAPI official tutorial). Its usage is basically similar to ResponseModel.

`response_model` parameter:

```python{1,3}
@router.get('/test', response_model=ResponseSchemaModel[GetApiDetail])
def test():
    return ResponseSchemaModel[GetApiDetail](data=GetApiDetail(...))
```

`->` type:

```python{2,3}
@router.get('/test')
def test() -> ResponseSchemaModel[GetApiDetail]:
    return ResponseSchemaModel[GetApiDetail](data=GetApiDetail(...))
```

Now let's take another look at the Swagger docs:

![response_schema_model](/images/response_schema_model.png)

We can see that the data in the response Schema now contains our response body structure. The response body structure is parsed from the Schema model in `[]`. They correspond. If the returned data structure doesn't match the
Schema, it will cause a parsing error.

We recommend using this method only for query APIs. If you don't need this documentation, you can completely avoid using it and instead use the more open unified response model
ResponseModel.

## Unified Response Method

`response_base` is a global response instance we created that greatly simplifies the response return method. Usage is as follows:

```python{2-3,7-8}
@router.get('/test')
def test() -> ResponseModel:
    return response_base.success(data={'test': 'test'})


@router.get('/test')
def test() -> ResponseSchemaModel[GetApiDetail]:
    return response_base.success(data=GetApiDetail(...))
```

This instance contains three return methods: `success()`, `fail()`, `fast_success()`

::: warning
They are all synchronous methods, not asynchronous. Because these return methods don't involve IO operations, defining them as asynchronous not only provides no performance improvement but also increases async coroutine overhead.
:::

::: tabs
@tab <Icon name="ix:success-filled" />`success()`

This method is usually used as the default response method. Default return information is as follows:

```json:no-line-numbers
{
  "code": 200,
  "msg": "Request successful",
  "data": null
}
```

@tab <Icon name="ix:namur-failure-filled" />`fail()`

This method is usually used when the API response information indicates failure. Default return information is as follows:

```json:no-line-numbers
{
  "code": 400,
  "msg": "Request error",
  "data": null
}
```

@tab <Icon name="ix:certificate-success-filled" />`fast_success()`

This method is usually only used when the API returns large json. It can bring qualitative improvements to json parsing performance. Default return information is as follows:

```json:no-line-numbers
{
  "code": 200,
  "msg": "Request successful",
  "data": null
}
```

:::

## Response Status Code

In the file `backend/common/response/response_code.py`, multiple ways to define response status codes are built-in. We can define our own needed response status codes according to `CustomResponseCode` and
`CustomResponse`, because in actual projects, response status codes have no unified standard.

After we define custom response status codes, we can use them like this:

```python{3-4}
@router.get('/test')
def test() -> ResponseModel:
    res = CustomResponse(code=0, msg='Success')
    return ResponseModel(res=res, data={'test': 'test'})
```

## CamelCase Response

We use Python's underscore naming convention for data returns by default. However, in actual work, frontend projects mostly use lower camelCase naming, so we need to make some modifications to adapt to frontend projects. In the file
`backend/common/schema.py`, we have a `SchemaBase` class, which is our global Schema base class. Modify as follows:

```python
class SchemaBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,  # [!code ++] Allow assignment through original field name or alias
        alias_generator=to_camel,  # [!code ++] Automatically convert field names to lower camelCase
        use_enum_values=True,
        json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)},
    )
```

Where `to_camel` method is imported from
pydantic. Details: [pydantic.alias_generators](https://docs.pydantic.dev/latest/api/config/#pydantic.alias_generators)

After completing the above modifications, Schema mode and returned data will automatically convert to lower camelCase naming.

## Internationalization

[Please refer to **Internationalization**](./i18n.md){.read-more}
