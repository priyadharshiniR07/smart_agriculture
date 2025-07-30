provider "aws" {
  region = "ap-southeast-2"
}


resource "aws_instance" "app_server" {
  ami           = "ami-010876b9ddd38475e" # Ubuntu 22.04 LTS in ap-south-1
  instance_type = "t2.micro"
  key_name      = "myec-2" # Replace with your actual key name

  vpc_security_group_ids = [aws_security_group.allow_web.id]

  user_data = <<-EOF
              #!/bin/bash
              apt update -y
              apt install -y docker.io
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ubuntu
              docker run -d -p 5000:5000 priyadharshiniR07/agriculture-docker-app
              EOF

  tags = {
    Name = "SmartAgricultureApp"
  }
}

resource "aws_security_group" "allow_web" {
  name        = "allow_web"
  description = "Allow HTTP & Flask"

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
