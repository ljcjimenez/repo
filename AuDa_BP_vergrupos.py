import pulumi
import pulumi_aws as aws

# 1. DEFINICIÓN DEL SECURITY GROUP
sec_group = aws.ec2.SecurityGroup('web-secgrp',
    description='Enable HTTP access',
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol='tcp',
            from_port=80,
            to_port=80,
            cidr_blocks=['0.0.0.0/0'],
        ),
        # Regla opcional para SSH (puerto 22) si tienes una llave configurada
    ],
)

# 2. SCRIPT DE INICIO (User Data)
# Este script se ejecuta la primera vez que el servidor arranca
user_data = """#!/bin/bash
sudo yum update -y
sudo yum install -y python3 git
echo "Servidor de Tesis listo" > /var/www/html/index.html
"""

# 3. INSTANCIA EC2 CON USER DATA
instancia = aws.ec2.Instance("servidor-pruebas-aws",
    instance_type="t3.micro",
    ami="ami-03ea746da1a2e36e7", # ID correcto para Ohio
    vpc_security_group_ids=[sec_group.id],
    user_data=user_data # Automatización de software
)

# 4. PLAN DE BACKUP (Respaldo automático)
vault = aws.backup.Vault("tesis-vault")
plan = aws.backup.Plan("tesis-backup-plan",
    rules=[aws.backup.PlanRuleArgs(
        rule_name="DailyBackup",
        target_vault_name=vault.name,
        schedule="cron(0 12 * * ? *)", # Se ejecuta a las 12:00 UTC
    )]
)

# SELECCIÓN DEL RECURSO A RESPALDAR
selection = aws.backup.Selection("tesis-selection",
    plan_id=plan.id,
    resources=[instancia.arn]
)

# EXPORTAR DATOS FINALES
pulumi.export('public_ip', instancia.public_ip)
pulumi.export('backup_vault_name', vault.name)