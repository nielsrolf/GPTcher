from aws_cdk import Stack
from aws_cdk import aws_certificatemanager as certificatemanager
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_elasticloadbalancingv2 as elb
from aws_cdk import aws_iam as iam
from aws_cdk import aws_secretsmanager as sm
from constructs import Construct
import os
from dotenv import load_dotenv

load_dotenv(override=True)

certificate_arn = "arn:aws:acm:eu-central-1:802148339218:certificate/76f01897-cc04-4c79-b935-0a616370816d"


class CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC and Subnets for the ECS Cluster
        vpc = ec2.Vpc(
            self,
            "VPC",
            max_azs=2,
        )

        # Create middleware ecs cluster
        image = ecs.ContainerImage.from_asset(
            directory=".",
            build_args={"platform": "linux/amd64"},
        )

        role = iam.Role(
            self,
            "FargateContainerRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        )
        role.add_to_policy(iam.PolicyStatement(actions=["sqs:*"], resources=["*"]))

        certificate = certificatemanager.Certificate.from_certificate_arn(
            self, "pollinationsworker", certificate_arn
        )

        # Create ECS pattern for the ECS Cluster
        cluster = ecs_patterns.ApplicationLoadBalancedFargateService(  # noqa
            self,
            "gptcher-api",
            vpc=vpc,
            public_load_balancer=True,
            protocol=elb.ApplicationProtocol.HTTPS,
            certificate=certificate,
            redirect_http=True,
            desired_count=1,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=image,
                container_port=5000,
                environment={
                    "DEBUG": "True",
                    "LOG_LEVEL": "DEBUG",
                    "LOG_FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    "SUPABASE_URL": os.environ["SUPABASE_URL"],
                    "SUPABASE_KEY": os.environ["SUPABASE_KEY"],
                    "JWT_SECRET": os.environ["JWT_SECRET"]
                },
                task_role=role,
            ),
            memory_limit_mib=1024,
            cpu=256,
        )  # noqa: F841


        