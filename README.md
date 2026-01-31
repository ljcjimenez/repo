# AWS Infrastructure Automation with Pulumi & Python 🚀

Este proyecto implementa una arquitectura de nube automatizada en **AWS** utilizando **Infraestructura como Código (IaC)** con **Pulumi** y **Python**. Está diseñado para desplegar entornos de pruebas escalables, seguros y con políticas de respaldo automáticas.

## 🏗️ Arquitectura del Proyecto

La infraestructura desplegada incluye:
* **Amazon EC2**: Instancia `t3.micro` aprovisionada dinámicamente en la región de Ohio (`us-east-2`).
* **Security Groups**: Configuración de reglas perimetrales para habilitar acceso HTTP (puerto 80).
* **User Data Automation**: Script de arranque que automatiza la actualización del sistema e instalación de **Python 3** y **Git**.
* **AWS Backup Plan**: Implementación de una bóveda de seguridad (`Vault`) y un plan de respaldo diario para asegurar la continuidad de los datos.



## 🛠️ Requisitos Previos

* **Pulumi CLI** instalado y configurado.
* **Python 3.10+** y `pip`.
* Cuenta de AWS activa con credenciales configuradas.

## 🚀 Guía de Despliegue

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/ljcjimenez/AWS-Pulumi-Infrastructure.git](https://github.com/TU_USUARIO/AWS-Pulumi-Infrastructure.git)
   cd AWS-Pulumi-Infrastructure