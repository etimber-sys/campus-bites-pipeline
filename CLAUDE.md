# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Campus Bites Pipeline is a Docker-based PostgreSQL setup for analyzing food delivery order data. It spins up a Postgres 16 database, loads a CSV of 1,131 orders into a single `orders` table, and exposes it locally for SQL analysis.

## Commands

### Database lifecycle
```bash
# Start the database (detached)
docker compose up -d

# Stop the database
docker compose down

# Full reset — wipes the volume and reloads all data
docker compose down -v && docker compose up -d
```

### Load data manually
```bash
# Requires Python venv with dependencies installed
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python load_data.py
```

### Connect to the database
```bash
# psql inside the running container
docker exec -it campus-bites-pipeline-db-1 psql -U postgres -d campus_bites
```

Connection string: `postgresql://postgres:postgres@localhost:5432/campus_bites`

## Architecture

```
docker-compose.yml
  └── PostgreSQL 16 service (campus_bites DB, port 5432)
        ├── ./data/ volume → /data inside container
        └── pgdata named volume (persistence)

load_data.py
  ├── reads data/campus_bites_orders.csv via pandas
  ├── connects to Postgres via psycopg2
  ├── CREATE TABLE IF NOT EXISTS orders (...)
  └── batch-inserts rows with executemany()
```

The data loader is **idempotent** — safe to re-run; it will not duplicate rows because the table uses `order_id` as a primary key and `CREATE TABLE IF NOT EXISTS`.

## Database Schema

Single table: `orders`

| Column | Type |
|---|---|
| order_id | INTEGER (PK) |
| order_date | DATE |
| order_time | TIME |
| customer_segment | VARCHAR |
| order_value | NUMERIC |
| cuisine_type | VARCHAR |
| delivery_time_mins | INTEGER |
| promo_code_used | BOOLEAN |
| is_reorder | BOOLEAN |

**Customer segments:** Grad Student, Off-Campus, Greek Life, Dorm
**Cuisine types:** Asian, Indian, Breakfast, Pizza, Mediterranean, Burgers
