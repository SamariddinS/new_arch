---
title: Why Choose Us?
---

<script setup>
import NpmBadge from 'vuepress-theme-plume/features/NpmBadge.vue'
</script>

> [!TIP]
> This repository is published as a template. Individuals and companies can use it freely.

> [!IMPORTANT]
> We don’t compare against other architectures. Each has its strengths and is suited to different scenarios.
>
> That said, FBA is arguably one of the cleanest, most standardized, and most elegant open-source architectures. {.important}

## Goals

Our aim is to provide a best-in-class architecture that lets developers get productive quickly, focus on business logic, or draw inspiration to optimize their own designs. We continuously refine this architecture to deliver a great developer experience.

## Commitment

This repository is published as a template and is free to use for individuals and companies. You can choose editions via the pricing page: ../../pricing.md

## Architecture

Unique, self-developed, and approachable architecture: the Quasi Three-Layer Architecture: ../summary/intro.md#quasi-three-layer-architecture

## Openness

- MIT license with fully open-sourced architecture code
- GitHub template repository for easy duplication and custom naming
- Nothing is hardcoded to the `fba` prefix; rename via your IDE as needed

## Flexibility

Our plugin system is the hallmark of flexibility. Beyond that, API responses, error types, and the architecture itself are designed to be practical and simple—developer-friendly by design.

## Long-term Maintenance

We’ve invested significant time since inception—and continue to do so.

![Alt](https://repobeats.axiom.co/api/embed/b2174ef1abbebaea309091f1c998fc97d0c1536a.svg "Repo beats analytics image")

## Origin

We once had a detailed issue describing FBA’s origin, but it was accidentally deleted and couldn’t be recovered despite contacting GitHub support.

In short, before FBA was created, our core member [downdawn](https://github.com/downdawn) found its predecessor [fastapi_sqlalchemy_mysql](fsm.md#sqlalchemy) and opened an issue “Some discussions and suggestions”. After days of discussion, we decided to create FBA.

## Related Tooling

Along the way, we created several related toolkits with zero coupling—you can use them in any compatible project.

<CardGrid>
  <LinkCard
    title="sqlalchemy-crud-plus"
    description="Advanced Asynchronous CRUD SDK Built on SQLAlchemy 2.0"
    href="https://github.com/fastapi-practices/sqlalchemy-crud-plus"
    icon="https://wu-clan.github.io/picx-images-hosting/logo/fba.png"
  />
  <LinkCard
    title="fastapi-oauth20"
    description="Asynchronous Authorization for OAuth 2.0 Clients in FastAPI"
    href="https://github.com/fastapi-practices/fastapi-oauth20"
    icon="https://wu-clan.github.io/picx-images-hosting/logo/fba.png"
  />
</CardGrid>

::: center
[more...](https://github.com/orgs/fastapi-practices/repositories?)
:::

## Slim Edition

Despite efforts to keep coupling low, a lightweight version still requires removing many parts. We provide a slim edition here: ./fsm.md

## Quality and Standards

- Use reStructuredText docstrings globally
  We adopt the reST style, a popular Python documentation format well-supported by IDEs.

- Track new framework features quickly
  We embrace new features from FastAPI and integrate them when stable and useful.

- Strict code quality
  We enforce rigorous CI checks with Ruff, guided by backend/.ruff.toml.

- Ongoing validation
  We don’t push marketing. Ask around in any community—we welcome authentic feedback.
