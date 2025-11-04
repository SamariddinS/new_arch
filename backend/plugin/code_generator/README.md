> [!TIP]
> The current version only includes backend code generation

> [!WARNING]
> Due to jinja2's text-based template rendering, the `preview` interface may have formatting issues and may not provide an intuitive code preview. This is a preset for the frontend

## Introduction

The code generator is implemented via API calls and includes two modules. The design may have defects. Please submit issues directly for related problems

### 1. Code Generation Business

Contains configuration related to code generation. For details, see: `generator/model/gen_business.py`

### 2. Code Generation Model Columns

Contains model column information required for code generation, just like defining normal model columns. Currently supported features are limited

## Usage

1. Start the backend service and operate directly from the swagger documentation
2. Send API requests through third-party API debugging tools
3. Start both frontend and backend simultaneously and operate from the page

Interface parameters mostly have descriptions. Please pay attention to them

### F. Fully Manual Mode

Not recommended (the manual business creation interface is marked as "deprecated")

1. Manually add a business entry through the business creation interface
2. Manually add model columns through the model creation interface
3. Access the `preview` (preview), `generate` (disk write), `download` (download) interfaces to perform backend code generation tasks

### S. Automatic Mode

Recommended

1. Access the `tables` interface to get the list of database table names
2. Through the `import` interface, import existing database table data, which will automatically create business table data and model table data
3. Access the `preview` (preview), `generate` (disk write), `download` (download) interfaces to perform backend code generation tasks
