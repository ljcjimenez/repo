# 1. Crear el .gitignore para proteger tus credenciales de AWS
@'
# Credenciales y archivos sensibles
*.csv
*.pub
mi-llave-aws
state.json
~*.docx
~$*.tmp
.pulumi/
'@ | Out-File -FilePath .gitignore -Encoding utf8

# 2. Corregir la URL del repositorio remoto
git remote set-url origin https://github.com/ljcjimenez/repo.git

# 3. Preparar los archivos y actualizar el README (simulado en el commit)
git add .
git commit -m "Fix: Configuración de seguridad .gitignore y corrección de URLs en README"

# 4. Sincronizar con GitHub (Pull con rebase para unir el historial antiguo)
git pull origin main --rebase

# 5. Subir la versión final
git push -u origin main