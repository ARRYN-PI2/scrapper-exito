# 📘 Guía de Uso del Exito Scraper

Esta guía está dirigida a diferentes roles que trabajarán con el scraper de productos de Éxito.

## Tabla de Contenidos

- [Para Ejecutores del Scraper](#-para-ejecutores-del-scraper)
- [Para Desarrolladores](#-para-desarrolladores)
- [Para Arquitectos de AWS](#️-para-arquitectos-de-aws)
- [Configuración Avanzada](#-configuración-avanzada)
- [Monitoreo y Troubleshooting](#-monitoreo-y-troubleshooting)

---

## Para Ejecutores del Scraper

### Ejecución Rápida con Docker (Recomendado)

#### 1. Ejecutar el scraper con Docker Compose:
```bash
# Extraer productos de una categoría
docker-compose run --rm exito-scraper scrape --categoria televisores --paginas 5

# Extraer múltiples categorías
docker-compose run --rm exito-scraper scrape --categoria "computadores portatiles" --paginas 3
docker-compose run --rm exito-scraper scrape --categoria "celulares" --paginas 2
```

#### 2. Ejecutar con Docker directamente:
```bash
# Construir la imagen
docker build -t exito-scraper .

# Ejecutar el scraper
docker run --rm -v $(pwd)/data:/app/data exito-scraper scrape --categoria televisores --paginas 5
```

### Ejecución Local (Sin Docker)

#### 1. Preparar el entorno:
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar Python path
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

#### 2. Ejecutar el scraper:
```bash
# Comando básico
python -m exito_scraper.main scrape --categoria televisores --paginas 3

# Con archivo de salida específico
python -m exito_scraper.main scrape --categoria "computadores portatiles" --paginas 5 --output data/computadores.jsonl
```

### Automatización con Cron

Para ejecutar el scraper automáticamente:

```bash
# Editar crontab
crontab -e

# Agregar estas líneas para ejecutar diariamente a las 6 AM
0 6 * * * cd /ruta/al/scraper && docker-compose run --rm exito-scraper scrape --categoria televisores --paginas 5
0 6 * * * cd /ruta/al/scraper && docker-compose run --rm exito-scraper scrape --categoria "computadores portatiles" --paginas 3
```

### Verificar Resultados

```bash
# Ver archivos generados
ls -la data/

# Contar productos extraídos
wc -l data/*.jsonl

# Ver formato de salida
head -n 1 data/productos.jsonl | python -m json.tool
```

---

## Para Desarrolladores

### Estructura del Proyecto

```
scrapper-exito/
├── exito_scraper/              # Código principal
│   ├── adapters/               # Adaptadores (scraper, repos)
│   ├── application/            # Casos de uso
│   ├── domain/                 # Modelos de dominio
│   ├── utils/                  # Utilidades (HTML cleaning)
│   └── main.py                 # CLI principal
├── data/                       # Datos extraídos
├── Dockerfile                  # Imagen Docker
├── docker-compose.yml          # Orquestación
└── requirements.txt            # Dependencias Python
```

### Desarrollo Local

#### 1. Configurar entorno de desarrollo:
```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Instalar en modo desarrollo
pip install -e .
```

#### 2. Ejecutar tests:
```bash
# Tests unitarios
python -m pytest tests/ -v

# Tests de integración
python -m pytest tests/integration/ -v

# Coverage
python -m pytest --cov=exito_scraper tests/
```

#### 3. Agregar nuevas categorías:
```python
# En exito_scraper/config.py
CATEGORIAS_DISPONIBLES = {
    'televisores': 'televisores',
    'computadores': 'computadores-portatiles',
    'nueva_categoria': 'url-categoria-nueva'
}
```

#### 4. Modificar campos extraídos:
```python
# En exito_scraper/domain/producto.py
@dataclass
class Producto:
    titulo: str
    precio: str
    # Agregar nuevo campo
    nuevo_campo: str = ""
```

### Debugging

```bash
# Ejecutar con logs detallados
PYTHONPATH=. python -m exito_scraper.main scrape --categoria televisores --paginas 1 --debug

# Usar debugger
import pdb; pdb.set_trace()
```

### Build y Deploy

```bash
# Construir imagen Docker
docker build -t exito-scraper:latest .

# Ejecutar tests en Docker
docker run --rm exito-scraper:latest python -m pytest

# Push a registry
docker tag exito-scraper:latest your-registry/exito-scraper:v1.0.0
docker push your-registry/exito-scraper:v1.0.0
```

---

## Para Arquitectos de AWS

### Arquitectura Recomendada - EC2 con Contenedores

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   EventBridge   │───▶│   Lambda     │───▶│   EC2 Instance  │
│   (Scheduler)   │    │  (Trigger)   │    │   + Docker      │
└─────────────────┘    └──────────────┘    └─────────────────┘
                                                     │
                                                     ▼
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   CloudWatch    │◀───│      S3      │◀───│  Systems Manager│
│    (Logs)       │    │   (Storage)  │    │   (Commands)    │
└─────────────────┘    └──────────────┘    └─────────────────┘
```

### 1. Configuración de Instancia EC2

#### User Data Script para EC2:
```bash
#!/bin/bash
# ec2-userdata.sh

# Instalar Docker
yum update -y
yum install -y docker
service docker start
usermod -a -G docker ec2-user

# Instalar Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Instalar AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install

# Instalar CloudWatch Agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
rpm -U ./amazon-cloudwatch-agent.rpm

# Crear directorio de trabajo
mkdir -p /opt/exito-scraper
cd /opt/exito-scraper

# Descargar código desde S3 o ECR
aws s3 cp s3://your-bucket/exito-scraper.tar.gz .
tar -xzf exito-scraper.tar.gz

# Configurar logging
cat > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json << 'EOF'
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/opt/exito-scraper/logs/*.log",
            "log_group_name": "/aws/ec2/exito-scraper",
            "log_stream_name": "{instance_id}/scraper.log"
          }
        ]
      }
    }
  }
}
EOF

# Iniciar CloudWatch Agent
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json -s
```

#### Instance Configuration (`launch-template.json`):
```json
{
  "LaunchTemplateName": "exito-scraper-template",
  "LaunchTemplateData": {
    "ImageId": "ami-0abcdef1234567890",
    "InstanceType": "t3.medium",
    "IamInstanceProfile": {
      "Name": "ExitoScraperInstanceProfile"
    },
    "SecurityGroupIds": ["sg-12345678"],
    "UserData": "base64-encoded-userdata-script",
    "TagSpecifications": [
      {
        "ResourceType": "instance",
        "Tags": [
          {"Key": "Name", "Value": "exito-scraper-instance"},
          {"Key": "Environment", "Value": "production"}
        ]
      }
    ],
    "BlockDeviceMappings": [
      {
        "DeviceName": "/dev/xvda",
        "Ebs": {
          "VolumeSize": 20,
          "VolumeType": "gp3",
          "DeleteOnTermination": true
        }
      }
    ]
  }
}
```

#### Deploy Script para EC2:
```bash
#!/bin/bash
# deploy-ec2.sh

# Variables
INSTANCE_NAME="exito-scraper-instance"
LAUNCH_TEMPLATE="exito-scraper-template"
KEY_PAIR="your-key-pair"
SUBNET_ID="subnet-12345678"

# Crear Launch Template
aws ec2 create-launch-template --cli-input-json file://launch-template.json

# Lanzar instancia
INSTANCE_ID=$(aws ec2 run-instances \
  --launch-template LaunchTemplateName=$LAUNCH_TEMPLATE \
  --subnet-id $SUBNET_ID \
  --query 'Instances[0].InstanceId' --output text)

echo "Instancia creada: $INSTANCE_ID"

# Esperar a que esté corriendo
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Obtener IP pública
PUBLIC_IP=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)

echo "Instancia lista en: $PUBLIC_IP"
echo "Conectar con: ssh -i $KEY_PAIR.pem ec2-user@$PUBLIC_IP"
```

### 2. Automatización con Systems Manager

#### SSM Document para ejecutar scraper:
```json
{
  "schemaVersion": "2.2",
  "description": "Ejecutar Exito Scraper en instancia EC2",
  "parameters": {
    "categoria": {
      "type": "String",
      "description": "Categoría a extraer",
      "default": "televisores"
    },
    "paginas": {
      "type": "String",
      "description": "Número de páginas",
      "default": "5"
    }
  },
  "mainSteps": [
    {
      "action": "aws:runShellScript",
      "name": "runExitoScraper",
      "inputs": {
        "timeoutSeconds": "3600",
        "runCommand": [
          "cd /opt/exito-scraper",
          "docker-compose run --rm exito-scraper scrape --categoria {{categoria}} --paginas {{paginas}}",
          "aws s3 cp data/ s3://your-bucket/data/$(date +%Y-%m-%d)/ --recursive --exclude '*' --include '*.jsonl'",
          "echo 'Scraper execution completed successfully'"
        ]
      }
    }
  ]
}
```

### 3. Automatización con EventBridge + Lambda

#### Lambda Function para trigger:
```python
# lambda_trigger.py
import boto3
import json

def lambda_handler(event, context):
    ssm = boto3.client('ssm')
    
    # Obtener instancias del scraper
    ec2 = boto3.client('ec2')
    instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Name', 'Values': ['exito-scraper-instance']},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    
    instance_ids = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
    
    if not instance_ids:
        return {
            'statusCode': 404,
            'body': json.dumps('No se encontraron instancias del scraper')
        }
    
    # Ejecutar comando SSM
    response = ssm.send_command(
        InstanceIds=instance_ids,
        DocumentName='ExitoScraperDocument',
        Parameters={
            'categoria': [event.get('categoria', 'televisores')],
            'paginas': [str(event.get('paginas', 5))]
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Scraper execution initiated',
            'command_id': response['Command']['CommandId']
        })
    }
```

#### EventBridge Rule:
```json
{
  "Rules": [
    {
      "Name": "ExitoScraperDaily",
      "ScheduleExpression": "cron(0 6 * * ? *)",
      "State": "ENABLED",
      "Targets": [
        {
          "Id": "1",
          "Arn": "arn:aws:lambda:region:account:function:exito-scraper-trigger",
          "Input": "{\"categoria\": \"televisores\", \"paginas\": 5}"
        }
      ]
    }
  ]
}
```

### 4. Almacenamiento en S3

#### Configuración de bucket:
```bash
# Crear bucket
aws s3 mb s3://exito-scraper-data

# Configurar lifecycle
aws s3api put-bucket-lifecycle-configuration \
  --bucket exito-scraper-data \
  --lifecycle-configuration file://lifecycle.json
```

#### `lifecycle.json`:
```json
{
  "Rules": [
    {
      "ID": "ArchiveOldData",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ]
    }
  ]
}
```

### 5. Monitoreo con CloudWatch

#### Configurar alarmas:
```bash
# Crear alarmas para instancia EC2
aws cloudwatch put-metric-alarm \
  --alarm-name "ExitoScraperInstanceDown" \
  --alarm-description "Monitor EC2 instance status" \
  --metric-name StatusCheckFailed \
  --namespace AWS/EC2 \
  --statistic Maximum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0

# Alarma para comandos SSM fallidos
aws cloudwatch put-metric-alarm \
  --alarm-name "ExitoScraperSSMFailures" \
  --alarm-description "Monitor SSM command failures" \
  --metric-name CommandsFailed \
  --namespace AWS/SSM-RunCommand \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold
```

### 6. IAM Roles y Políticas

#### EC2 Instance Role (`ec2-instance-role.json`):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::exito-scraper-data",
        "arn:aws:s3:::exito-scraper-data/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogStreams"
      ],
      "Resource": "arn:aws:logs:*:*:log-group:/aws/ec2/exito-scraper"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssm:UpdateInstanceInformation",
        "ssm:SendCommand",
        "ssm:ListCommandInvocations"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:PutMetricData"
      ],
      "Resource": "*"
    }
  ]
}
```

### 7. Terraform Configuration para EC2

```hcl
# main.tf
resource "aws_instance" "exito_scraper" {
  ami                    = "ami-0abcdef1234567890"  # Amazon Linux 2
  instance_type          = "t3.medium"
  key_name              = var.key_pair_name
  subnet_id             = var.subnet_id
  vpc_security_group_ids = [aws_security_group.exito_scraper.id]
  iam_instance_profile   = aws_iam_instance_profile.exito_scraper.name
  
  user_data = base64encode(templatefile("${path.module}/userdata.sh", {
    s3_bucket = aws_s3_bucket.exito_scraper_data.bucket
  }))
  
  root_block_device {
    volume_type = "gp3"
    volume_size = 20
    encrypted   = true
  }
  
  tags = {
    Name        = "exito-scraper-instance"
    Environment = var.environment
    Project     = "exito-scraper"
  }
}

resource "aws_security_group" "exito_scraper" {
  name_prefix = "exito-scraper-"
  vpc_id      = var.vpc_id
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.ssh_allowed_cidr_blocks
  }
  
  tags = {
    Name = "exito-scraper-sg"
  }
}

resource "aws_s3_bucket" "exito_scraper_data" {
  bucket = "exito-scraper-data-${random_string.suffix.result}"
  
  tags = {
    Name        = "exito-scraper-data"
    Environment = var.environment
  }
}

resource "aws_lambda_function" "exito_scraper_trigger" {
  filename         = "lambda_trigger.zip"
  function_name    = "exito-scraper-trigger"
  role            = aws_iam_role.lambda_execution_role.arn
  handler         = "lambda_trigger.lambda_handler"
  runtime         = "python3.9"
  timeout         = 300
  
  environment {
    variables = {
      INSTANCE_TAG_NAME = "exito-scraper-instance"
      SSM_DOCUMENT_NAME = "ExitoScraperDocument"
    }
  }
}

resource "aws_cloudwatch_event_rule" "exito_scraper_schedule" {
  name                = "exito-scraper-daily"
  description         = "Trigger exito scraper daily at 6 AM"
  schedule_expression = "cron(0 6 * * ? *)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.exito_scraper_schedule.name
  target_id = "ExitoScraperLambdaTarget"
  arn       = aws_lambda_function.exito_scraper_trigger.arn
  
  input = jsonencode({
    categoria = "televisores"
    paginas   = 5
  })
}
```

---

## Configuración Avanzada

### Variables de Entorno

```bash
# .env
SCRAPER_DELAY=2                    # Delay entre requests (segundos)
SCRAPER_RETRIES=3                  # Número de reintentos
SCRAPER_TIMEOUT=30                 # Timeout de requests
OUTPUT_FORMAT=both                 # jsonl, json, both
LOG_LEVEL=INFO                     # DEBUG, INFO, WARNING, ERROR
USER_AGENT="Custom Bot 1.0"       # User agent personalizado
PROXY_URL=""                       # URL del proxy (opcional)
```

### Configuración de Rate Limiting

```python
# En exito_scraper/config.py
RATE_LIMIT_CONFIG = {
    'requests_per_minute': 30,
    'delay_between_requests': 2.0,
    'exponential_backoff': True,
    'max_retries': 3
}
```

---

## Monitoreo y Troubleshooting

### Logs y Debugging en EC2

```bash
# Conectar a la instancia
ssh -i your-key.pem ec2-user@your-instance-ip

# Ver logs del scraper
tail -f /opt/exito-scraper/logs/scraper.log

# Ver logs de CloudWatch Agent
tail -f /opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log

# Verificar estado del Docker
docker ps -a
docker logs exito-scraper-container
```

### Métricas Importantes para EC2

1. **CPU y memoria de la instancia EC2**
2. **Espacio en disco disponible**
3. **Comandos SSM ejecutados exitosamente**
4. **Productos extraídos por ejecución**
5. **Tiempo de ejecución del scraper**

### Troubleshooting Específico para EC2

#### Problema: "Instancia EC2 no responde"
```bash
# Verificar estado de la instancia
aws ec2 describe-instances --instance-ids i-1234567890abcdef0

# Reiniciar instancia si es necesario
aws ec2 reboot-instances --instance-ids i-1234567890abcdef0

# Verificar conectividad SSH
ssh -i your-key.pem ec2-user@your-instance-ip "echo 'Connection OK'"
```

#### Problema: "SSM Command falla"
```bash
# Verificar agente SSM
aws ssm describe-instance-information --filters "Key=InstanceIds,Values=i-1234567890abcdef0"

# Ver historial de comandos
aws ssm list-command-invocations --instance-id i-1234567890abcdef0

# Reiniciar agente SSM en la instancia
sudo systemctl restart amazon-ssm-agent
```

#### Problema: "Docker no está disponible"
```bash
# En la instancia EC2
sudo service docker status
sudo service docker start
sudo usermod -a -G docker ec2-user

# Verificar imágenes Docker
docker images
docker pull your-registry/exito-scraper:latest
```

### Comandos de Monitoreo

```bash
# Verificar ejecución del scraper
aws ssm send-command \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["cd /opt/exito-scraper && docker-compose ps"]' \
  --targets "Key=tag:Name,Values=exito-scraper-instance"

# Ver métricas de CloudWatch
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --start-time 2025-08-28T00:00:00Z \
  --end-time 2025-08-28T23:59:59Z \
  --period 3600 \
  --statistics Average
```

---

## Soporte

- **Código fuente**: Ver documentación en el código
- **Issues**: Reportar problemas en el repositorio
- **Logs**: Siempre incluir logs completos al reportar problemas
- **AWS CloudWatch**: Monitorear métricas de la instancia EC2
- **SSH Access**: Conectar directamente a la instancia para debugging

---

*Última actualización: Agosto 2025*
