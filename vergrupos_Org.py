import pulumi
import pulumi_aws as aws

# 1. Definir el Security Group PRIMERO
sec_group = aws.ec2.SecurityGroup('web-secgrp',
    description='Enable HTTP access',
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol='tcp',
            from_port=80,
            to_port=80,
            cidr_blocks=['0.0.0.0/0'],
        ),
    ],
)

# 2. Crear la instancia usando el ID de Ohio y el grupo definido arriba
instancia = aws.ec2.Instance("servidor-pruebas-aws",
    instance_type="t3.micro",
    ami="ami-03ea746da1a2e36e7", # ID correcto para us-east-2
    vpc_security_group_ids=[sec_group.id] 
)

# 3. Exportar la IP para que aparezca en 'stack output'
pulumi.export('public_ip', instancia.public_ip) 