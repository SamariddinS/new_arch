# Database-Level i18n Implementation Plan

## Executive Summary

This plan outlines the integration of database-level internationalization (i18n) into the FastAPI Best Architecture (FBA) project. The solution will enable models to store translatable content in the database and automatically return translations based on the `Accept-Language` header, while maintaining backward compatibility with the existing file-based i18n system.

---

## Table of Contents

1. [Current State Analysis](#1-current-state-analysis)
2. [Proposed Solution Architecture](#2-proposed-solution-architecture)
3. [Technical Implementation Strategy](#3-technical-implementation-strategy)
4. [Database Schema Design](#4-database-schema-design)
5. [Model Layer Implementation](#5-model-layer-implementation)
6. [Service Layer Integration](#6-service-layer-integration)
7. [API Layer Changes](#7-api-layer-changes)
8. [Migration Strategy](#8-migration-strategy)
9. [Testing Strategy](#9-testing-strategy)
10. [Performance Considerations](#10-performance-considerations)
11. [Implementation Roadmap](#11-implementation-roadmap)

---

## 1. Current State Analysis

### 1.1 Existing i18n System

**Architecture:** File-based translation system
- **Location:** `backend/locale/` directory
- **Formats:** JSON (en-US.json) and YAML (ru-RU.yml)
- **Languages:** English (en-US), Russian (ru-RU)
- **Default Language:** `ru-RU` (configurable in `backend/core/conf.py`)

**Language Detection:**
- Middleware: `I18nMiddleware` (`backend/middleware/i18n_middleware.py`)
- Reads `Accept-Language` header
- Maps to locale codes (e.g., `en` → `en-US`, `ru` → `ru-RU`)
- Sets global `i18n.current_language`

**Translation Function:**
```python
from backend.common.i18n import t

# Usage: t('response.success') → "Request success"
message = t('error.captcha.expired')
```

**Current Usage:**
- API response messages (`response.success`, `response.error`)
- Error messages (`error.captcha.expired`)
- Pydantic validation errors (comprehensive in Russian, minimal in English)
- Authentication success messages

### 1.2 Database Configuration

- **Default Database:** PostgreSQL 16.0+ (since v1.10.0)
- **Also Supports:** MySQL 8.0+
- **ORM:** SQLAlchemy 2.0 (async)
- **Session Management:** `CurrentSession` (auto-commit), `CurrentSessionTransaction` (with transaction)
- **JSON Support:** Already using `sa.JSON()` in models (opera_log, task_scheduler)

### 1.3 Model Patterns

**Base Classes:**
- `MappedBase` - Basic declarative base
- `DataClassBase` - With dataclass integration
- `Base` - With timestamps (created_time, updated_time)

**Custom Types:**
- `UniversalText` - Compatible with both PostgreSQL (Text) and MySQL (LONGTEXT)

**Key Models Requiring i18n:**

| Priority | Model | File | Translatable Fields |
|----------|-------|------|---------------------|
| **CRITICAL** | Menu | `backend/app/admin/model/menu.py` | `title`, `name`, `remark` |
| **CRITICAL** | DictData | `backend/plugin/dict/model/dict_data.py` | `label`, `remark` |
| **HIGH** | DictType | `backend/plugin/dict/model/dict_type.py` | `name`, `remark` |
| **HIGH** | Role | `backend/app/admin/model/role.py` | `name`, `remark` |
| **MEDIUM** | Department | `backend/app/admin/model/dept.py` | `name` |
| **MEDIUM** | Config | `backend/plugin/config/model/config.py` | `name`, `remark` |
| **MEDIUM** | Notice | `backend/plugin/notice/model/notice.py` | `title`, `content` |

### 1.4 Architecture Gaps

**Current Limitations:**
1. **No database-level translations** - All content is monolingual
2. **Concurrency issue** - Global `i18n.current_language` can conflict in concurrent requests
3. **No context storage** - Language not stored in request context (`ctx`)
4. **Manual management** - Adding new translatable fields requires code changes

---

## 2. Proposed Solution Architecture

### 2.1 Hybrid Approach

Combine the existing file-based system with database-level translations:

1. **File-based i18n** (existing) - For static content:
   - API response messages
   - Error messages
   - Validation messages
   - System messages

2. **Database-level i18n** (new) - For dynamic content:
   - Menu titles and names
   - Dictionary labels
   - Role names
   - Department names
   - Configuration names
   - User-generated content

### 2.2 Technology Choice: JSON Columns

**Selected Approach:** PostgreSQL JSON columns with fallback support

**Rationale:**
- ✅ Native PostgreSQL support (already using JSON in other models)
- ✅ No additional dependencies (unlike SQLAlchemy-Utils TranslationHybrid)
- ✅ MySQL compatibility through JSON type
- ✅ Simple schema (no separate translation tables)
- ✅ Query flexibility (can filter by specific language)
- ✅ Backward compatible (can keep existing string columns)

**JSON Structure:**
```json
{
  "en-US": "English text",
  "ru-RU": "Русский текст",
  "es-ES": "Texto en español"
}
```

**Alternative Considered:** Separate translation tables (rejected due to complexity and performance)

### 2.3 Key Design Principles

1. **Backward Compatibility:** Existing non-translated fields continue to work
2. **Graceful Degradation:** Falls back to default language if translation missing
3. **Request-Scoped Language:** Store language in request context
4. **Hybrid Properties:** Automatic translation in model layer
5. **Migration Path:** Gradual model-by-model migration
6. **Admin Support:** UI for managing translations

---

## 3. Technical Implementation Strategy

### 3.1 Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    Accept-Language Header                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│           I18nMiddleware (Enhanced)                              │
│  - Detect language from header                                   │
│  - Set ctx.language (NEW)                                        │
│  - Set i18n.current_language (existing)                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│           Request Context (ctx)                                  │
│  - ctx.language = 'en-US'                                        │
│  - Available throughout request lifecycle                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│           Model Layer                                            │
│  - JSON columns: name_translations, title_translations           │
│  - Hybrid properties: name, title (auto-translate)               │
│  - Fallback to default language                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│           Schema Layer                                           │
│  - Return translated values in responses                         │
│  - Accept translations in create/update requests                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│           API Response                                           │
│  - Localized content based on Accept-Language                    │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Language Resolution Flow

```python
# Priority order for translation lookup:
1. Check ctx.language (from Accept-Language header)
2. Check JSON translations[ctx.language]
3. Fall back to I18N_DEFAULT_LANGUAGE
4. Fall back to first available translation
5. Return None or empty string
```

---

## 4. Database Schema Design

### 4.1 Translation Column Naming Convention

**Pattern:** `{field_name}_translations`

Examples:
- `name` → `name_translations`
- `title` → `title_translations`
- `label` → `label_translations`
- `content` → `content_translations`

### 4.2 JSON Column Type

**PostgreSQL:**
```python
from sqlalchemy import JSON

name_translations: Mapped[dict[str, str] | None] = mapped_column(
    JSON,
    nullable=True,
    comment='Name translations {locale: text}'
)
```

**MySQL Compatible:**
```python
from sqlalchemy import JSON

name_translations: Mapped[dict[str, str] | None] = mapped_column(
    JSON,
    nullable=True,
    comment='Name translations {locale: text}'
)
```

### 4.3 Example Schema Transformation

**Before (Menu model):**
```python
class Menu(Base):
    __tablename__ = 'sys_menu'

    id: Mapped[id_key] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(String(64), comment='Menu title')
    name: Mapped[str] = mapped_column(String(64), comment='Menu name')
```

**After (with i18n):**
```python
from sqlalchemy import JSON
from backend.common.context import ctx
from backend.core.conf import settings

class Menu(Base):
    __tablename__ = 'sys_menu'

    id: Mapped[id_key] = mapped_column(init=False)

    # Original columns (kept for backward compatibility)
    title: Mapped[str] = mapped_column(String(64), comment='Menu title (default language)')
    name: Mapped[str] = mapped_column(String(64), comment='Menu name (default language)')

    # NEW: Translation storage columns
    title_translations: Mapped[dict[str, str] | None] = mapped_column(
        JSON,
        nullable=True,
        comment='Title translations {locale: text}'
    )
    name_translations: Mapped[dict[str, str] | None] = mapped_column(
        JSON,
        nullable=True,
        comment='Name translations {locale: text}'
    )

    # NEW: Hybrid properties for automatic translation
    @hybrid_property
    def title_i18n(self) -> str:
        """Get localized title based on current request language"""
        return get_translation(
            self.title_translations,
            fallback=self.title,
            language=getattr(ctx, 'language', None)
        )

    @hybrid_property
    def name_i18n(self) -> str:
        """Get localized name based on current request language"""
        return get_translation(
            self.name_translations,
            fallback=self.name,
            language=getattr(ctx, 'language', None)
        )
```

### 4.4 Migration Script Template

```python
"""Add i18n support to menu table

Revision ID: xxxx
Revises: yyyy
Create Date: 2024-xx-xx
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import JSON

def upgrade() -> None:
    # Add translation columns
    op.add_column('sys_menu', sa.Column('title_translations', JSON, nullable=True, comment='Title translations'))
    op.add_column('sys_menu', sa.Column('name_translations', JSON, nullable=True, comment='Name translations'))

    # Optional: Migrate existing data to translations
    # This can be done in a separate data migration script

def downgrade() -> None:
    op.drop_column('sys_menu', 'name_translations')
    op.drop_column('sys_menu', 'title_translations')
```

---

## 5. Model Layer Implementation

### 5.1 Translation Utility Module

**Location:** `backend/common/db_i18n.py` (NEW FILE)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Database-level internationalization utilities"""

from typing import Any

from backend.common.context import ctx
from backend.core.conf import settings


def get_translation(
    translations: dict[str, str] | None,
    fallback: str | None = None,
    language: str | None = None,
) -> str:
    """
    Get translation for the current request language

    :param translations: Dictionary of translations {locale: text}
    :param fallback: Fallback text if no translation found
    :param language: Override language (uses ctx.language if None)
    :return: Translated text or fallback
    """
    if not translations:
        return fallback or ''

    # Determine language to use
    if language is None:
        language = getattr(ctx, 'language', None)

    if language is None:
        language = settings.I18N_DEFAULT_LANGUAGE

    # Try exact match
    if language in translations:
        return translations[language]

    # Try default language
    if settings.I18N_DEFAULT_LANGUAGE in translations:
        return translations[settings.I18N_DEFAULT_LANGUAGE]

    # Return first available translation
    if translations:
        return next(iter(translations.values()))

    # Final fallback
    return fallback or ''


def set_translation(
    translations: dict[str, str] | None,
    language: str,
    text: str,
) -> dict[str, str]:
    """
    Set or update a translation for a specific language

    :param translations: Existing translations dictionary
    :param language: Language code (e.g., 'en-US')
    :param text: Translated text
    :return: Updated translations dictionary
    """
    if translations is None:
        translations = {}

    translations[language] = text
    return translations


def remove_translation(
    translations: dict[str, str] | None,
    language: str,
) -> dict[str, str] | None:
    """
    Remove a translation for a specific language

    :param translations: Existing translations dictionary
    :param language: Language code to remove
    :return: Updated translations dictionary
    """
    if translations is None:
        return None

    translations.pop(language, None)
    return translations if translations else None


def get_all_translations(translations: dict[str, str] | None) -> dict[str, str]:
    """
    Get all available translations

    :param translations: Translations dictionary
    :return: All translations or empty dict
    """
    return translations or {}
```

### 5.2 Translatable Mixin

**Location:** `backend/common/model.py` (ADD TO EXISTING FILE)

```python
from sqlalchemy import JSON
from sqlalchemy.ext.hybrid import hybrid_property
from backend.common.db_i18n import get_translation


class TranslatableMixin:
    """
    Mixin for models with translatable fields

    Usage:
        class MyModel(Base, TranslatableMixin):
            name: Mapped[str] = mapped_column(String(64))
            name_translations: Mapped[dict[str, str] | None] = mapped_column(JSON, nullable=True)

            # Auto-generated by mixin:
            # name_i18n property
    """

    @classmethod
    def _get_translatable_fields(cls) -> list[str]:
        """
        Override this to specify which fields are translatable

        :return: List of field names (without _translations suffix)
        """
        return []

    def __init_subclass__(cls, **kwargs):
        """Automatically create hybrid properties for translatable fields"""
        super().__init_subclass__(**kwargs)

        # Auto-detect translation fields by looking for *_translations columns
        for attr_name in dir(cls):
            if attr_name.endswith('_translations'):
                base_name = attr_name[:-13]  # Remove '_translations'

                # Create hybrid property
                def make_hybrid(field_base_name):
                    @hybrid_property
                    def _hybrid(self) -> str:
                        translations = getattr(self, f'{field_base_name}_translations', None)
                        fallback = getattr(self, field_base_name, None)
                        return get_translation(translations, fallback=fallback)

                    return _hybrid

                # Set the hybrid property on the class
                i18n_property = make_hybrid(base_name)
                setattr(cls, f'{base_name}_i18n', i18n_property)
```

### 5.3 Example Model Implementation

**Menu Model** (`backend/app/admin/model/menu.py`):

```python
from __future__ import annotations

from sqlalchemy import JSON, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key, TranslatableMixin
from backend.common.db_i18n import get_translation
from backend.common.context import ctx


class Menu(Base, TranslatableMixin):
    """Menu Model"""

    __tablename__ = 'sys_menu'

    id: Mapped[id_key] = mapped_column(init=False)

    # Original fields (for backward compatibility and default values)
    title: Mapped[str] = mapped_column(
        String(64),
        comment='Menu title (default language)'
    )
    name: Mapped[str] = mapped_column(
        String(64),
        comment='Menu name (default language)'
    )

    # Translation storage
    title_translations: Mapped[dict[str, str] | None] = mapped_column(
        JSON,
        nullable=True,
        comment='Title translations {locale: text}'
    )
    name_translations: Mapped[dict[str, str] | None] = mapped_column(
        JSON,
        nullable=True,
        comment='Name translations {locale: text}'
    )

    # Other fields...
    path: Mapped[str | None] = mapped_column(String(200), comment='Route path')
    # ... rest of existing fields ...

    # Hybrid properties (auto-generated by TranslatableMixin)
    # - title_i18n
    # - name_i18n
```

---

## 6. Service Layer Integration

### 6.1 CRUD Operations

**Reading Data:**
```python
# In CRUD layer - no changes needed
# The hybrid property handles translation automatically

async def get_menu(db: AsyncSession, menu_id: int) -> Menu | None:
    """Get menu by ID"""
    result = await db.execute(
        select(Menu).where(Menu.id == menu_id)
    )
    return result.scalar_one_or_none()
```

**Creating Data:**
```python
async def create_menu(
    db: AsyncSession,
    obj_in: MenuCreateSchema
) -> Menu:
    """Create new menu with translations"""
    menu = Menu(
        title=obj_in.title,  # Default language
        name=obj_in.name,    # Default language
        title_translations=obj_in.title_translations,  # Optional translations
        name_translations=obj_in.name_translations,    # Optional translations
        # ... other fields
    )
    db.add(menu)
    await db.flush()
    return menu
```

**Updating Data:**
```python
async def update_menu(
    db: AsyncSession,
    menu: Menu,
    obj_in: MenuUpdateSchema
) -> Menu:
    """Update menu with translations"""
    # Update standard fields
    if obj_in.title is not None:
        menu.title = obj_in.title

    # Update translations
    if obj_in.title_translations is not None:
        menu.title_translations = obj_in.title_translations

    await db.flush()
    return menu
```

### 6.2 Service Layer

**No changes required** - Services work with models transparently:

```python
# In service layer
async def get_menu_tree(db: AsyncSession, language: str | None = None) -> list[dict]:
    """Get menu tree with translations"""
    menus = await menu_crud.get_all(db)

    # Accessing .title_i18n automatically returns translated value
    return [
        {
            'id': menu.id,
            'title': menu.title_i18n,  # ← Automatically translated
            'name': menu.name_i18n,    # ← Automatically translated
            'path': menu.path,
        }
        for menu in menus
    ]
```

---

## 7. API Layer Changes

### 7.1 Schema Updates

**Location:** `backend/app/admin/schema/menu.py`

**Base Schema (for responses):**
```python
from pydantic import Field

class MenuSchemaBase(SchemaBase):
    """Menu base schema"""

    # Standard fields
    title: str = Field(description='Menu title (localized if available)')
    name: str = Field(description='Menu name (localized if available)')
    path: str | None = Field(default=None, description='Route path')

    # Optional: Include all translations in response
    title_translations: dict[str, str] | None = Field(
        default=None,
        description='All title translations {locale: text}'
    )
    name_translations: dict[str, str] | None = Field(
        default=None,
        description='All name translations {locale: text}'
    )
```

**Create Schema:**
```python
class MenuCreateSchema(MenuSchemaBase):
    """Menu create schema"""

    # Default language values (required)
    title: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=64)

    # Translations (optional)
    title_translations: dict[str, str] | None = Field(
        default=None,
        description='Title translations (e.g., {"en-US": "Dashboard", "ru-RU": "Панель"})'
    )
    name_translations: dict[str, str] | None = Field(
        default=None,
        description='Name translations'
    )
```

**Update Schema:**
```python
class MenuUpdateSchema(SchemaBase):
    """Menu update schema"""

    title: str | None = None
    name: str | None = None
    title_translations: dict[str, str] | None = None
    name_translations: dict[str, str] | None = None
```

### 7.2 Response Formatting

**Option A: Return localized values only (simpler)**
```python
from backend.common.response.response_schema import ResponseSchemaModel

@router.get('/{pk}', response_model=ResponseSchemaModel[MenuSchemaBase])
async def get_menu(pk: int, db: CurrentSession):
    """Get menu by ID"""
    menu = await menu_service.get(db, pk)

    # Convert to schema - use i18n properties
    return ResponseSchemaModel(data={
        'id': menu.id,
        'title': menu.title_i18n,  # ← Localized
        'name': menu.name_i18n,    # ← Localized
        'path': menu.path,
    })
```

**Option B: Return all translations (more flexible)**
```python
@router.get('/{pk}', response_model=ResponseSchemaModel[MenuSchemaBase])
async def get_menu(pk: int, db: CurrentSession):
    """Get menu by ID with all translations"""
    menu = await menu_service.get(db, pk)

    return ResponseSchemaModel(data={
        'id': menu.id,
        'title': menu.title_i18n,              # ← Current language
        'name': menu.name_i18n,                # ← Current language
        'title_translations': menu.title_translations,  # ← All translations
        'name_translations': menu.name_translations,    # ← All translations
        'path': menu.path,
    })
```

### 7.3 New Translation Management Endpoints

**Location:** `backend/app/admin/api/v1/sys/menu.py`

```python
@router.put('/{pk}/translations', summary='Update menu translations')
async def update_translations(
    pk: int,
    translations: MenuTranslationsUpdateSchema,
    db: CurrentSession,
):
    """
    Update translations for a specific menu

    Request body:
    {
        "title_translations": {
            "en-US": "Dashboard",
            "ru-RU": "Панель управления",
            "es-ES": "Tablero"
        },
        "name_translations": {
            "en-US": "dashboard",
            "ru-RU": "панель",
            "es-ES": "tablero"
        }
    }
    """
    menu = await menu_service.get(db, pk)
    if not menu:
        raise NotFoundError(msg='Menu not found')

    menu.title_translations = translations.title_translations
    menu.name_translations = translations.name_translations

    await db.flush()
    return response_base.success(msg='Translations updated')


@router.get('/{pk}/translations', summary='Get all translations for menu')
async def get_translations(pk: int, db: CurrentSession):
    """Get all available translations for a menu"""
    menu = await menu_service.get(db, pk)
    if not menu:
        raise NotFoundError(msg='Menu not found')

    return response_base.success(data={
        'title_translations': menu.title_translations or {},
        'name_translations': menu.name_translations or {},
    })
```

---

## 8. Migration Strategy

### 8.1 Phase 1: Infrastructure Setup

**Tasks:**
1. Add `language` to request context (`backend/common/context.py`)
2. Update `I18nMiddleware` to set `ctx.language`
3. Create `backend/common/db_i18n.py` utility module
4. Add `TranslatableMixin` to `backend/common/model.py`
5. Add configuration for enabled languages in `backend/core/conf.py`

**Files to Modify:**
- `backend/common/context.py`
- `backend/middleware/i18n_middleware.py`
- `backend/common/db_i18n.py` (new)
- `backend/common/model.py`
- `backend/core/conf.py`

### 8.2 Phase 2: Model Migration (Per-Model)

**Order of Implementation:**

1. **Menu** (highest priority)
   - Add `title_translations`, `name_translations` columns
   - Create Alembic migration
   - Update schema
   - Update API endpoints
   - Test with multiple languages

2. **DictData** (critical for UI)
   - Add `label_translations` column
   - Migrate existing labels if needed
   - Update dict plugin APIs

3. **DictType** (dictionary categories)
   - Add `name_translations` column

4. **Role** (admin UI)
   - Add `name_translations` column

5. **Department** (organizational structure)
   - Add `name_translations` column

6. **Config** (system parameters)
   - Add `name_translations` column

7. **Notice** (user notifications)
   - Add `title_translations`, `content_translations` columns

**Per-Model Checklist:**
- [ ] Create Alembic migration adding `*_translations` columns
- [ ] Update model class with JSON columns
- [ ] Update schemas (create/update/response)
- [ ] Update CRUD operations (if needed)
- [ ] Update service layer (if needed)
- [ ] Update API endpoints
- [ ] Add translation management endpoints
- [ ] Write tests
- [ ] Update documentation

### 8.3 Phase 3: Data Migration

**For existing data**, create data migration scripts:

```python
"""Migrate existing menu data to translations

Revision ID: data_xxxx
Revises: schema_xxxx
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    # Get default language from config
    default_lang = 'ru-RU'  # Or read from settings

    # Migrate menu titles and names
    session.execute(sa.text(f"""
        UPDATE sys_menu
        SET
            title_translations = jsonb_build_object(:lang, title),
            name_translations = jsonb_build_object(:lang, name)
        WHERE title_translations IS NULL
    """), {'lang': default_lang})

    session.commit()

def downgrade() -> None:
    # Clear translations
    bind = op.get_bind()
    session = Session(bind=bind)

    session.execute(sa.text("""
        UPDATE sys_menu
        SET title_translations = NULL, name_translations = NULL
    """))

    session.commit()
```

### 8.4 Phase 4: Admin UI Enhancement (Optional)

**Frontend components for translation management:**
1. Translation editor component
2. Language selector in forms
3. Bulk translation import/export
4. Translation coverage dashboard

---

## 9. Testing Strategy

### 9.1 Unit Tests

**Location:** `backend/tests/test_db_i18n.py` (new)

```python
import pytest
from backend.common.db_i18n import get_translation, set_translation
from backend.common.context import ctx

class TestTranslationUtils:
    """Test database i18n utilities"""

    def test_get_translation_with_exact_match(self):
        """Test translation retrieval with exact language match"""
        translations = {
            'en-US': 'Dashboard',
            'ru-RU': 'Панель управления',
        }

        ctx.language = 'en-US'
        assert get_translation(translations) == 'Dashboard'

        ctx.language = 'ru-RU'
        assert get_translation(translations) == 'Панель управления'

    def test_get_translation_with_fallback(self):
        """Test fallback to default language"""
        translations = {
            'ru-RU': 'Панель управления',
        }

        ctx.language = 'es-ES'  # Not available
        result = get_translation(translations, fallback='Default')
        assert result == 'Панель управления'  # Falls back to first available

    def test_get_translation_empty(self):
        """Test with no translations"""
        ctx.language = 'en-US'
        assert get_translation(None, fallback='Fallback') == 'Fallback'

    def test_set_translation(self):
        """Test setting translations"""
        translations = {'en-US': 'Old'}
        translations = set_translation(translations, 'ru-RU', 'Новый')

        assert translations == {
            'en-US': 'Old',
            'ru-RU': 'Новый',
        }
```

### 9.2 Integration Tests

**Location:** `backend/tests/test_api/test_v1/test_menu_i18n.py` (new)

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestMenuI18n:
    """Test menu i18n functionality"""

    async def test_create_menu_with_translations(self, client: AsyncClient):
        """Test creating menu with multiple translations"""
        response = await client.post(
            '/api/v1/menus',
            json={
                'title': 'Dashboard',  # Default
                'name': 'dashboard',
                'title_translations': {
                    'en-US': 'Dashboard',
                    'ru-RU': 'Панель управления',
                    'es-ES': 'Tablero',
                },
                'name_translations': {
                    'en-US': 'dashboard',
                    'ru-RU': 'панель',
                    'es-ES': 'tablero',
                },
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data['data']['title'] == 'Dashboard'

    async def test_get_menu_with_language_header(self, client: AsyncClient, menu_id: int):
        """Test menu retrieval with different Accept-Language headers"""
        # English
        response = await client.get(
            f'/api/v1/menus/{menu_id}',
            headers={'Accept-Language': 'en-US'},
        )
        assert response.json()['data']['title'] == 'Dashboard'

        # Russian
        response = await client.get(
            f'/api/v1/menus/{menu_id}',
            headers={'Accept-Language': 'ru-RU'},
        )
        assert response.json()['data']['title'] == 'Панель управления'

        # Spanish
        response = await client.get(
            f'/api/v1/menus/{menu_id}',
            headers={'Accept-Language': 'es-ES'},
        )
        assert response.json()['data']['title'] == 'Tablero'

    async def test_update_translations(self, client: AsyncClient, menu_id: int):
        """Test updating menu translations"""
        response = await client.put(
            f'/api/v1/menus/{menu_id}/translations',
            json={
                'title_translations': {
                    'fr-FR': 'Tableau de bord',
                },
            },
        )
        assert response.status_code == 200

        # Verify French translation works
        response = await client.get(
            f'/api/v1/menus/{menu_id}',
            headers={'Accept-Language': 'fr-FR'},
        )
        assert response.json()['data']['title'] == 'Tableau de bord'
```

### 9.3 Performance Tests

**Load testing for translation queries:**
```python
async def test_translation_performance(db: AsyncSession):
    """Ensure translations don't significantly impact query performance"""
    import time

    # Without translations
    start = time.time()
    menus = await db.execute(select(Menu).limit(100))
    baseline = time.time() - start

    # With translations
    start = time.time()
    menus = await db.execute(select(Menu).limit(100))
    for menu in menus.scalars():
        _ = menu.title_i18n  # Access translated property
    with_i18n = time.time() - start

    # Ensure overhead is minimal (< 20%)
    assert with_i18n < baseline * 1.2
```

---

## 10. Performance Considerations

### 10.1 Database Indexing

**For frequently queried translations:**

```sql
-- PostgreSQL GIN index for JSON searches
CREATE INDEX idx_menu_title_translations ON sys_menu USING GIN (title_translations);

-- Query specific language efficiently
SELECT * FROM sys_menu WHERE title_translations->>'en-US' = 'Dashboard';
```

### 10.2 Caching Strategy

**Add Redis caching for translated content:**

```python
from backend.database.redis import redis_client
import json

async def get_menu_with_cache(
    db: AsyncSession,
    menu_id: int,
    language: str
) -> dict:
    """Get menu with Redis caching"""
    cache_key = f'menu:{menu_id}:{language}'

    # Try cache first
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Query database
    menu = await menu_crud.get(db, menu_id)
    result = {
        'id': menu.id,
        'title': menu.title_i18n,
        'name': menu.name_i18n,
    }

    # Cache for 1 hour
    await redis_client.setex(cache_key, 3600, json.dumps(result))

    return result
```

### 10.3 Query Optimization

**Load translations selectively:**

```python
# Only load translation columns when needed
stmt = select(
    Menu.id,
    Menu.title,
    Menu.title_translations,  # Only if needed
)

# Use defer() to skip translation columns in list views
from sqlalchemy.orm import defer

stmt = select(Menu).options(
    defer(Menu.title_translations),
    defer(Menu.name_translations),
)
```

### 10.4 Pagination with Translations

**Ensure pagination works efficiently:**

```python
from backend.common.pagination import paging_data

# Translations don't affect pagination performance
stmt = select(Menu).order_by(Menu.created_time.desc())
page_data = await paging_data(db, stmt)

# Access translations in serialization step
items = [
    {
        'id': menu.id,
        'title': menu.title_i18n,
    }
    for menu in page_data['items']
]
```

---

## 11. Implementation Roadmap

### Timeline: 4-6 Weeks

#### Week 1: Infrastructure & Planning
- [ ] Review and approve this plan
- [ ] Set up development branch
- [ ] Implement core infrastructure:
  - [ ] Add `ctx.language` to context
  - [ ] Update `I18nMiddleware`
  - [ ] Create `db_i18n.py` utilities
  - [ ] Add `TranslatableMixin`
- [ ] Write unit tests for utilities
- [ ] Update configuration

#### Week 2: Menu Model Migration (POC)
- [ ] Create Alembic migration for Menu model
- [ ] Update Menu model with translations
- [ ] Update Menu schemas
- [ ] Update Menu API endpoints
- [ ] Add translation management endpoints
- [ ] Write integration tests
- [ ] Test with real data
- [ ] Documentation

#### Week 3: Dictionary Plugin Migration
- [ ] Migrate DictData model
- [ ] Migrate DictType model
- [ ] Update dict plugin APIs
- [ ] Data migration scripts
- [ ] Update dict plugin tests
- [ ] Verify backward compatibility

#### Week 4: Role & Department Migration
- [ ] Migrate Role model
- [ ] Migrate Department model
- [ ] Update admin APIs
- [ ] Integration testing
- [ ] Performance testing

#### Week 5: Config & Notice Migration
- [ ] Migrate Config model
- [ ] Migrate Notice model
- [ ] Update plugin APIs
- [ ] End-to-end testing
- [ ] Load testing

#### Week 6: Documentation & Deployment
- [ ] Complete API documentation
- [ ] Write developer guide
- [ ] Create migration guide for existing deployments
- [ ] Prepare release notes
- [ ] Code review
- [ ] Merge to main branch

---

## Appendices

### A. Configuration Changes

**Add to `backend/core/conf.py`:**

```python
# I18n configuration
I18N_DEFAULT_LANGUAGE: str = 'ru-RU'

# NEW: List of supported languages
I18N_SUPPORTED_LANGUAGES: list[str] = ['en-US', 'ru-RU', 'es-ES', 'fr-FR']

# NEW: Enable database-level i18n
I18N_DB_ENABLED: bool = True

# NEW: Fallback behavior
I18N_FALLBACK_TO_DEFAULT: bool = True  # If True, fall back to default language
I18N_FALLBACK_TO_ANY: bool = True      # If True, return any available translation
```

### B. Context Changes

**Update `backend/common/context.py`:**

```python
class TypedContextProtocol(Protocol):
    perf_time: float
    start_time: datetime

    ip: str
    country: str | None
    region: str | None
    city: str | None

    user_agent: str
    os: str | None
    browser: str | None
    device: str | None

    permission: str | None

    # NEW: Language context
    language: str  # e.g., 'en-US', 'ru-RU'
```

### C. Middleware Changes

**Update `backend/middleware/i18n_middleware.py`:**

```python
from backend.common.context import ctx

class I18nMiddleware(BaseHTTPMiddleware):
    """Internationalized Middleware"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process requests and configure internationalization languages"""
        language = get_current_language(request)

        # Set International Language
        if language:
            i18n.current_language = language
            ctx.language = language  # NEW: Store in request context
        else:
            ctx.language = settings.I18N_DEFAULT_LANGUAGE  # NEW

        response = await call_next(request)
        return response
```

### D. SQLAlchemy JSON Type Reference

**PostgreSQL JSON vs JSONB:**

```python
# JSON - Stores as text, slower queries
from sqlalchemy import JSON
column: Mapped[dict] = mapped_column(JSON)

# JSONB - Binary storage, faster queries, supports indexing
from sqlalchemy.dialects.postgresql import JSONB
column: Mapped[dict] = mapped_column(JSONB)

# Recommendation: Use JSONB for PostgreSQL-only, JSON for MySQL compatibility
```

### E. Example API Request/Response

**Create Menu with Translations:**
```bash
POST /api/v1/menus
Accept-Language: en-US
Content-Type: application/json

{
  "title": "Dashboard",
  "name": "dashboard",
  "path": "/dashboard",
  "title_translations": {
    "en-US": "Dashboard",
    "ru-RU": "Панель управления",
    "es-ES": "Tablero",
    "fr-FR": "Tableau de bord"
  },
  "name_translations": {
    "en-US": "dashboard",
    "ru-RU": "панель",
    "es-ES": "tablero",
    "fr-FR": "tableau"
  }
}
```

**Response:**
```json
{
  "code": 200,
  "msg": "Success",
  "data": {
    "id": 1,
    "title": "Dashboard",
    "name": "dashboard",
    "path": "/dashboard",
    "title_translations": {
      "en-US": "Dashboard",
      "ru-RU": "Панель управления",
      "es-ES": "Tablero",
      "fr-FR": "Tableau de bord"
    },
    "name_translations": {
      "en-US": "dashboard",
      "ru-RU": "панель",
      "es-ES": "tablero",
      "fr-FR": "tableau"
    }
  }
}
```

**Get Menu with Russian Language:**
```bash
GET /api/v1/menus/1
Accept-Language: ru-RU
```

**Response:**
```json
{
  "code": 200,
  "msg": "Success",
  "data": {
    "id": 1,
    "title": "Панель управления",
    "name": "панель",
    "path": "/dashboard"
  }
}
```

---

## Conclusion

This plan provides a comprehensive, production-ready approach to integrating database-level internationalization into the FastAPI Best Architecture project. The hybrid approach maintains backward compatibility while adding powerful translation capabilities at the database level.

**Key Benefits:**
- ✅ Automatic translation based on `Accept-Language` header
- ✅ Backward compatible with existing code
- ✅ Simple JSON-based storage (no complex joins)
- ✅ Extensible to new models
- ✅ Works with existing PostgreSQL setup
- ✅ Minimal performance impact
- ✅ Clear migration path

**Next Steps:**
1. Review and approve this plan
2. Set up development branch: `claude/db-i18n-implementation`
3. Begin Week 1 infrastructure tasks
4. Implement Menu model as POC
5. Iterate based on feedback

---

**Document Version:** 1.0
**Date:** 2024-11-09
**Author:** Claude (Anthropic)
**Status:** Draft - Pending Approval
