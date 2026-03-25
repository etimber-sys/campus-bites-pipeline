# Campus Bites Pipeline

A local Postgres database for analyzing Campus Bites order data. Spin it up with one command — the database is created and the CSV is loaded automatically on first startup.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)

## Quickstart

```bash
docker compose up -d
```

That's it. On first run, Postgres will automatically execute the scripts in `sql/` in alphabetical order:

1. `init.sql` — creates the `orders` table and loads `data/campus_bites_orders.csv`

## Connecting

**Connection string:**
```
postgresql://postgres:postgres@localhost:5432/campus_bites
```

| Setting  | Value          |
|----------|----------------|
| Host     | localhost      |
| Port     | 5432           |
| Database | campus_bites   |
| User     | postgres       |
| Password | postgres       |

**GUI clients** (TablePlus, DBeaver, DataGrip) — use the settings above.

**psql (command line):**
```bash
docker exec -it campus-bites-pipeline-db-1 psql -U postgres -d campus_bites
```

## Table: `orders`

| Column              | Type           | Description                    |
|---------------------|----------------|--------------------------------|
| order_id            | INTEGER (PK)   | Unique order identifier        |
| order_date          | DATE           | Date the order was placed      |
| order_time          | TIME           | Time the order was placed      |
| customer_segment    | VARCHAR(50)    | e.g. Grad Student, Off-Campus  |
| order_value         | NUMERIC(10,2)  | Order total in dollars         |
| cuisine_type        | VARCHAR(50)    | e.g. Asian, Indian, Breakfast  |
| delivery_time_mins  | INTEGER        | Delivery duration in minutes   |
| promo_code_used     | VARCHAR(3)     | Yes / No                       |
| is_reorder          | VARCHAR(3)     | Yes / No                       |

## Example Queries

```sql
-- How many orders total?
SELECT COUNT(*) FROM orders;

-- Average order value by customer segment
SELECT customer_segment, ROUND(AVG(order_value), 2) AS avg_value
FROM orders
GROUP BY customer_segment
ORDER BY avg_value DESC;

-- Most popular cuisine types
SELECT cuisine_type, COUNT(*) AS order_count
FROM orders
GROUP BY cuisine_type
ORDER BY order_count DESC;

-- Promo code impact on order value
SELECT promo_code_used, ROUND(AVG(order_value), 2) AS avg_value
FROM orders
GROUP BY promo_code_used;

-- Average delivery time by cuisine
SELECT cuisine_type, ROUND(AVG(delivery_time_mins), 1) AS avg_delivery_mins
FROM orders
GROUP BY cuisine_type
ORDER BY avg_delivery_mins;
```

## Stopping and Resetting

**Stop the container (data is preserved):**
```bash
docker compose down
```

**Full reset — delete all data and reload from CSV on next startup:**
```bash
docker compose down -v
docker compose up -d
```

The `-v` flag removes the named volume (`pgdata`), which causes Postgres to treat the next startup as a fresh install and re-run the init scripts.

## Project Structure

```
campus-bites-pipeline/
├── data/
│   └── campus_bites_orders.csv   # Source data
├── sql/
│   └── init.sql                  # Creates the orders table and loads CSV
├── docker-compose.yml            # Postgres service definition
└── README.md
```
