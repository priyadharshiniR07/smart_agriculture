provider "aws" {
  region = "ap-southeast-2"
}

resource "aws_key_pair" "deployer" {
  key_name   = "myec2-key-${formatdate("YYYYMMDD", timestamp())}"
  public_key = file("C:/Users/Priyadharshini/.ssh/id_rsa.pub")
}

resource "aws_security_group" "app_sg" {
  name        = "flask-app1-sg-${formatdate("YYYYMMDD", timestamp())}"
  description = "Allow HTTP and SSH traffic"

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

resource "aws_instance" "app_server" {
  ami                    = "ami-010876b9ddd38475e" # Ubuntu 20.04 LTS
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.app_sg.id]

  user_data = file("${path.module}/user_data.sh")

  tags = {
    Name = "agricultureappserver"
  }
}

output "app_url" {
  value = "http://${aws_instance.app_server.public_ip}:8000"
}

output "ssh_command" {
  value = "ssh -i ~/.ssh/id_rsa ubuntu@${aws_instance.app_server.public_ip}"
}

output "instance_public_ip" {
  value = aws_instance.app_server.public_ip
}
