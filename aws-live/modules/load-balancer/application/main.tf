///////////////////////
// PROVIDER DEFINITION
///////////////////////


provider "aws" {
  region = var.aws_region
  access_key = var.access_key
  secret_key = var.secret_key
}


//////////////////////////////////////
// Application Load Balancer
// ToDo: Change bucket name
// TODo: Change Access Log Settings
// ToDO: Change Tags
// ToDo: Change delete protection
//////////////////////////////////////


//ToDo: This code will likely be not correct to monitor firewalls and will require fine tuning going forward


resource "aws_lb" "app_lb" {
  name = "${var.vpc_name}-App-LB"

//  vpc_id = "${var.vpc_id}" -- this doesn't look like a required parameter in this resource; confirm after 'apply'

  internal = var.lb_internal
  load_balancer_type = "application"
  security_groups = [var.security_group_id]
  subnets = [var.subnet_a_id, var.subnet_b_id]

  enable_deletion_protection = false
  enable_cross_zone_load_balancing = true

  access_logs {
    bucket = var.lb_access_log_bucket
    prefix = "app-lb"
    enabled = false
  }

  tags = {
    Environment = "production"
    Name = "${var.vpc_name}-App-LB"
  }
}

resource "aws_lb_target_group" "http_tg" {
  name        = "${var.vpc_name}-http-Target-Group"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    port = "traffic-port"
    healthy_threshold = "5"
    unhealthy_threshold = "2"
    timeout = "3"
    interval = "5"
    matcher = "200"
  }
}

resource "aws_lb_target_group_attachment" "fw1_http_tg_attach" {
  target_group_arn = aws_lb_target_group.http_tg.arn
  target_id        = var.instance1_ip
  port             = 80
}

resource "aws_lb_target_group_attachment" "fw2_http_tg_attach" {
  target_group_arn = aws_lb_target_group.http_tg.arn
  target_id        = var.instance2_ip
  port             = 80
}

resource "aws_lb_listener" "http_listener" {
  load_balancer_arn = aws_lb.app_lb.arn
  port = 80
  protocol = "HTTP"

  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.http_tg.arn
  }
}

resource "aws_lb_listener_rule" "http_rule" {
  listener_arn = aws_lb_listener.http_listener.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.http_tg.arn
  }

  condition {
    field  = "path-pattern"
    values = ["/"]
  }
}
