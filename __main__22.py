import pulumi
import pulumi_aws as aws

# 1. CARGAR LLAVE PÚBLICA (Asegúrate que el archivo existe en D:\AWS)
with open('./mi-llave-aws.pub', 'r') as pub_key_file:
    public_key_content = pub_key_file.read()

key_pair = aws.ec2.KeyPair("mi-llave-aws",
    public_key=public_key_content
)

# 2. BUSCAR AMI AUTOMÁTICAMENTE
ami_info = aws.ec2.get_ami(
    most_recent=True,
    owners=["137112412989"],
    filters=[aws.ec2.GetAmiFilterArgs(name="name", values=["al2023-ami-2023*-x86_64"])]
)

# 3. SECURITY GROUP (SSH + HTTP)
sec_group = aws.ec2.SecurityGroup('web-secgrp',
    description='Permitir SSH y HTTP',
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol='tcp', from_port=22, to_port=22, cidr_blocks=['0.0.0.0/0']
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol='tcp', from_port=80, to_port=80, cidr_blocks=['0.0.0.0/0']
        ),
    ],
    egress=[aws.ec2.SecurityGroupEgressArgs(
        protocol='-1', from_port=0, to_port=0, cidr_blocks=['0.0.0.0/0']
    )]
)

# 4. SCRIPT DE INSTALACIÓN AUTOMÁTICA (User Data)
# Este script instala Nginx y crea una página personalizada al arrancar
user_data = """#!/bash
dnf install nginx -y
systemctl start nginx
systemctl enable nginx
echo "<h1>Servidor desplegado con Pulumi por Lucky</h1>" > /usr/share/nginx/html/index.html
"""

# 5. CREAR INSTANCIA
instancia = aws.ec2.Instance("servidor-pruebas-aws",
    instance_type="t2.micro",
    ami=ami_info.id,
    key_name=key_pair.key_name,
    vpc_security_group_ids=[sec_group.id],
    user_data=user_data, # <--- Magia: Instalación automática
    tags={"Name": "servidor-pruebas-aws"}
)

# OUTPUTS
pulumi.export('ip_publica', instancia.public_ip)
pulumi.export('url_web', instancia.public_ip.apply(lambda ip: f"http://{ip}"))