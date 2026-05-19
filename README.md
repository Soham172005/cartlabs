# CartLabs

CartLabs is a production-style e-commerce platform scaffold built with a React + Tailwind CSS frontend, Django microservices, JWT authentication, Postgres and Docker Compose.

## Platform Architecture

| Layer | Service | Port | Responsibility |
| --- | --- | ---: | --- |
| Frontend | React + Tailwind | 5173 | Auth-gated shopping UI, catalog search, product detail, cart, billing and tracking screens |
| Gateway | Django API Gateway | 8000 | Single frontend API surface and request routing |
| Auth | Django | 8001 | Register, login, JWT issuing, authenticated profile |
| Product | Django | 8002 | Product listing, search, category filters and product details |
| Cart | Django | 8003 | User cart persistence |
| Recommendation | Django | 8004 | Similar product recommendations |
| Order | Django | 8005 | Billing details and order creation |
| Tracking | Django | 8006 | Order tracking timeline from placed to received |
| Database | Postgres | 5432 | Persistent data store |

## User Flow

1. Users always start at login. New users can switch to registration.
2. A valid login returns a JWT and opens the products page.
3. Users search products, filter by category, open product details and review similar product recommendations.
4. Users add multiple products to cart and review line totals and subtotal.
5. Users fill billing and delivery fields. No payment gateway is connected yet.
6. Placing an order creates an order and opens the tracking timeline from order placed to received.

## Run With Docker

```bash
docker compose up --build
```

Then open:

- Frontend: http://localhost:5173
- API gateway: http://localhost:8000/health

## AWS Production Infrastructure

Terraform for a low-cost single-instance AWS deployment lives in `infra/terraform`.

It provisions one `m5.large` EC2 instance in `ap-south-1`, installs Docker and Docker Compose, and avoids expensive managed services such as RDS, ALB, NAT Gateway and EIP.

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

After apply, SSH into the instance, copy or clone CartLabs into `/opt/cartlabs`, and run:

```bash
docker compose up -d --build
```

For production CI/CD deployments, Jenkins uses `docker-compose.prod.yml` to serve the frontend through Nginx on port `80`.

## CI/CD

The Jenkins pipeline is defined in `Jenkinsfile`.

It validates secrets, checks backend syntax, builds the frontend, validates Docker Compose and deploys to the EC2 instance over SSH. Setup details are in `docs/jenkins-cicd.md`.

## Local Development

Backend services are independent Django apps under `backend/`. Each service is built through the shared `backend/Dockerfile` using the `SERVICE_DIR` build argument.

Frontend source lives in `frontend/src/main.jsx` and uses `VITE_API_BASE_URL` for the gateway URL.

```bash
cd frontend
npm install
npm run dev
```

## Notes For Next Iterations

- Replace the in-code product seed data with product-service database models and admin/import tooling.
- Add payment provider integration behind the checkout form.
- Add async events between order and tracking services with Kafka, Redis Streams or RabbitMQ.
- Split Postgres into per-service databases for stricter production isolation.
- Add test suites for API contracts and checkout/cart regression coverage.
