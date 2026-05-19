output "instance_id" {
  description = "CartLabs EC2 instance ID."
  value       = aws_instance.cartlabs.id
}

output "public_ip" {
  description = "Public IP of the CartLabs EC2 instance."
  value       = aws_instance.cartlabs.public_ip
}

output "public_dns" {
  description = "Public DNS name of the CartLabs EC2 instance."
  value       = aws_instance.cartlabs.public_dns
}

output "ssh_command" {
  description = "SSH command template."
  value       = "ssh -i <path-to-private-key.pem> ubuntu@${aws_instance.cartlabs.public_ip}"
}

output "frontend_url" {
  description = "Temporary frontend URL while running Vite through Docker Compose."
  value       = "http://${aws_instance.cartlabs.public_ip}:5173"
}

output "api_gateway_url" {
  description = "API gateway URL."
  value       = "http://${aws_instance.cartlabs.public_ip}:8000"
}
