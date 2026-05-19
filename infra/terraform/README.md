# CartLabs Terraform

This Terraform stack creates the smallest AWS production target for CartLabs:

- 1 EC2 instance
- 1 security group
- Default VPC and default public subnet
- Docker Engine and Docker Compose installed through EC2 user data

It intentionally does not create RDS, ALB, NAT Gateway, EIP, ECS, EKS or Route 53 resources to keep AWS credit usage low.

## Region And Size

- Region: `ap-south-1`
- Instance: `m5.large`
- OS: latest Ubuntu 24.04 LTS AMI
- Disk: 30 GiB gp3 root volume

## Prerequisites

1. AWS credentials configured locally.
2. An existing EC2 key pair in `ap-south-1`.
3. Your public IP in CIDR form for SSH, for example `203.0.113.10/32`.

## Usage

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:

```hcl
key_name         = "your-existing-aws-keypair-name"
allowed_ssh_cidr = "YOUR_PUBLIC_IP/32"
```

Then run:

```bash
terraform init
terraform plan
terraform apply
```

## Deploy CartLabs On The Instance

SSH into the instance using the `ssh_command` output, then place the project in `/opt/cartlabs` and run:

```bash
cd /opt/cartlabs
docker compose up -d --build
```

The outputs include temporary URLs for:

- Frontend: `http://PUBLIC_IP`
- API gateway: `http://PUBLIC_IP:8000`

## Cost Control

Destroy the instance when not in use:

```bash
terraform destroy
```

Avoid adding NAT Gateway, Load Balancer, RDS or Elastic IP until you are ready to spend more.
