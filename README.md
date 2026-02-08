# WallStr.chat

[![Status](https://img.shields.io/badge/Status-Archived-red)](https://finanalytica.chat)
[![Migrated](https://img.shields.io/badge/Migrated_to-FinAnalytica.chat-blue)](https://finanalytica.chat)
[![License](https://img.shields.io/badge/New_Version-Proprietary%20SaaS-lightgrey)](https://finanalytica.chat)

> [!WARNING]
> **This repository is archived and no longer maintained.**
>
> The project has migrated to **[FinAnalytica.chat](https://finanalytica.chat)**.  
> Note: The new version has evolved into a proprietary service and is no longer open source.  
> You can use the live tool at the link above.

## Installation

1. Install [pnpm](https://pnpm.io/installation#using-npm)
2. Install [poetry](https://python-poetry.org/docs/#installation)
3. Install dependencies
   ```bash
   pnpm install
   poetry install -C packages/backend
   ```

## Running locally

1. Backend, check [backend/README.md](packages/backend/README.md) for more information

   ```bash
   pnpm docker-compose

   pnpm backend:dev
   pnpm backend:worker -p 1
   pnpm backend:worker:heavy -p 1
   ```

2. Frontend (setup `packages/frontend/.env` file first)

   ```bash
   pnpm frontend:dev
   ```

3. Open http://localhost:3000
