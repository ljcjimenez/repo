import pulumi
import pulumi_aws as aws

# 1. LEER LA LLAVE PÚBLICA 
# Asegúrate de haber ejecutado 'ssh-keygen -t rsa -f ./mi-llave-aws' antes
with open('./mi-llave-aws.pub', 'r') as pub_key_file:
    public_key_content = pub_key_file.read()

# 2. REGISTRAR LA LLAVE EN AWS
key_pair = aws.ec2.KeyPair("mi-llave-aws",
    public_key=public_key_content
)

# 3. BUSCAR LA AMI DE AMAZON LINUX 2023 AUTOMÁTICAMENTE
ami_info = aws.ec2.get_ami(
    most_recent=True,
    owners=["137112412989"],
    filters=[
        aws.ec2.GetAmiFilterArgs(
            name="name",
            values=["al2023-ami-2023*-x86_64"],
        ),
    ],
)

# 4. CREAR EL SECURITY GROUP (FIREWALL)
# Abrimos puerto 22 (SSH) y puerto 80 (HTTP para Nginx)
sec_group = aws.ec2.SecurityGroup('web-secgrp',
    description='Permitir SSH y trafico HTTP',
    ingress=[
        # Regla para SSH
        aws.ec2.SecurityGroupIngressArgs(
            protocol='tcp',
            from_port=22,
            to_port=22,
            cidr_blocks=['0.0.0.0/0'],
        ),
        # Regla para Web (Nginx)
        aws.ec2.SecurityGroupIngressArgs(
            protocol='tcp',
            from_port=80,
            to_port=80,
            cidr_blocks=['0.0.0.0/0'],
        ),
    ],
    egress=[
        # Permitir que el servidor salga a internet (necesario para instalar paquetes)
        aws.ec2.SecurityGroupEgressArgs(
            protocol='-1',
            from_port=0,
            to_port=0,
            cidr_blocks=['0.0.0.0/0'],
        ),
    ]
)

# 5. CREAR LA INSTANCIA EC2
instancia = aws.ec2.Instance("servidor-pruebas-aws",
    instance_type="t2.micro",
    ami=ami_info.id,
    key_name=key_pair.key_name, # Vincula la llave SSH
    vpc_security_group_ids=[sec_group.id], # Vincula el firewall
    tags={
        "Name": "servidor-pruebas-aws",
    }
)

# 6. OUTPUTS (Resultados en consola)
pulumi.export('public_ip', instancia.public_ip)
pulumi.export('url_web', instancia.public_ip.apply(lambda ip: f"http://{ip}"))
pulumi.export('comando_ssh', instancia.public_ip.apply(
    lambda ip: f"ssh -i ./mi-llave-aws ec2-user@{ip}"
))