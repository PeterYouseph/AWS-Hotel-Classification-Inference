# Desenvolvimento da aplicação Compass 

## 👨‍💻👩‍💻 Projeto desenvolvido por: [José Pedro Cândido L.P.](https://github.com/PeterYouseph) , [Pedro Montenegro](https://github.com/Montenegro-dev), [Natália Siqueira Cardoso](https://github.com/NataliaC-nala), e [Renan Mazzilli Dias](https://github.com/renan-mazzilli).

## 📚 Contextualização do projeto

Este projeto utiliza a AWS para treinar um modelo de machine learning que classifica reservas de hotéis em faixas de preço, utilizando o dataset do Kaggle. Os dados são processados e armazenados no DynamoDB, o modelo é treinado no SageMaker e salvo no S3. Um serviço de inferência em Python, desenvolvido com FastAPI, carrega o modelo do S3 e expõe um endpoint para previsões, registrando logs no DynamoDB. O serviço é containerizado com Docker e implantado no Elastic Beanstalk, acessível via API Gateway, garantindo escalabilidade e gerenciamento eficiente.

## 🖥️ Funcionamento do sistema

- Configuração do ambiente na AWS, incluindo serviços como DynamoDB, SageMaker, S3, Elastic Beanstalk e API Gateway.
- Leitura dos dados do Kaggle e armazenamento no DynamoDB.
- Pré-processamento e tratamento dos dados, com salvamento do dataset alterado no DynamoDB.
- Carregamento dos dados e treinamento do modelo no SageMaker, seguido de salvamento do modelo no S3.
- Desenvolvimento de um serviço em Python (FastAPI) para receber requisições POST, carregar o modelo salvo no S3, realizar a predição e retornar o resultado.
- Containerização do serviço com Docker e implantação no Elastic Beanstalk.

## 🛠️ Tecnologias/Ferramentas utilizadas

### Para a implementação do projeto, foram utilizadas as seguintes tecnologias/ferramentas: 

##### Bibliotecas e modelos do projeto:
- Random Forest
- XGBoost
- fastapi
- uvicorn
- boto3
- python-dotenv
- pandas
- scikit-learn
- xgboost
- numpy
- seaborn
- matplotlib
- sklearn
- joblib

##### Ferramentas para o desenvolvimento, versionamento e *deploy* do projeto:

[<img src="https://img.shields.io/badge/Visual_Studio_Code-007ACC?logo=visual-studio-code&logoColor=white">](https://code.visualstudio.com/)
[<img src="https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white">](https://git-scm.com/)
[<img src="https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white">](https://github.com/)
[<img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white">](https://www.docker.com/)
[<img src="https://img.shields.io/badge/AWS-232F3E?logo=amazon-aws&logoColor=white">](https://aws.amazon.com/pt/)
[<img src="https://img.shields.io/badge/AWS-CLI-232F3E?logo=amazon-aws&logoColor=white">](https://aws.amazon.com/pt/cli/)
[<img src="https://img.shields.io/badge/aws_ec2-232F3E?logo=amazon-aws&logoColor=white">](https://aws.amazon.com/pt/ec2/)
[<img src="https://img.shields.io/badge/aws_eb-232F3E?logo=amazon-aws&logoColor=white">](https://aws.amazon.com/pt/elasticbeanstalk/)
[<img src="https://img.shields.io/badge/aws_s3-232F3E?logo=amazon-aws&logoColor=white">](https://aws.amazon.com/pt/s3/)

##### Organização do Time:

[<img src="https://img.shields.io/badge/Trello-0079BF?logo=trello&logoColor=white">](https://trello.com/)
[<img src="https://img.shields.io/badge/Teams-6264A7?logo=microsoft-teams&logoColor=white">](https://www.microsoft.com/pt-br/microsoft-teams/group-chat-software)
[<img src="https://img.shields.io/badge/WhatsApp-25D366?logo=whatsapp&logoColor=white">](https://www.whatsapp.com/?lang=pt_br)

## 📁 Estrutura do projeto 

- ***`./docker-compose.yml` →*** Arquivo de configuração do Docker Compose para a execução do projeto.

- ***`./.dockerignore`*** → Arquivo que contém os diretórios e arquivos que serão ignorados pelo Docker.

## 📁 Estrutura da API

```bash
├── /api
│   ├── /controllers
│   │   ├── controller.py
│   │   ├──__init__.py 
│   ├── /models
│   │   ├── _init_.py
│   │   ├── dataModel.py
│   ├── /services
│   │   ├── accessS3Service.py
│   │   ├── credentialService.py
│   │   ├── inferenceLogsToDynamo.py
│   │   └── predictionService.py
│   └── /utils
│       ├── requirements.txt
│       └── api.py
├── assets
│   ├── dataset_schema.png
│   └── sprint4-5.jpg
├── notebooks
│   ├── dataset_preprocessing_upload.ipynb
│   ├── infrastructure_role_settings.ipynb
│   ├── locally_train_models.ipynb
│   └── sagemaker_train_model.ipynb
├──.gitignore
└── README.md
```

## 📌 Como executar a API localmente

### Clone o repositório

```bash
$ git clone https://github.com/Compass-pb-aws-2024-MARCO/sprints-4-5-pb-aws-marco.git
```

### Acesse a pasta do projeto no terminal/cmd:

```bash
$ cd sprints-4-5-pb-aws-marco
```

### Realize um check-out para a branch de desenvolvimento:

```bash
$ git checkout grupo-3
```
### Entre na pasta da API

```bash
$ cd api 
```

### Instale as dependências

```bash
$ pip install -r requirements.txt
```

### Execute a API

```bash
$ python3 api.py
```

## 📌 Como fazer a requisição

### Faça uma requisição POST para o endpoint <endereço-da-api>/api/v1/predict, o formato da requisição deve ser:

```bash
{
    "no_of_adults": 3,
    "no_of_children": 3,
    "type_of_meal_plan": "example"
    ...
}
```

## 🤯 Dificuldades encontradas 

### Dificuldades técnicas

#### Configuração do ambiente de produção no AWS Elastic Beanstalk com Docker

### Dificuldades de organização

#### Organização do time e divisão de tarefas
