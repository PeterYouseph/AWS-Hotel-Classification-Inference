# Avaliação Sprints 4 e 5 - Programa de Bolsas Compass UOL e AWS - Março/2024

Avaliação das quarta e quinta sprints do programa de bolsas Compass UOL para formação em machine learning para AWS.

***

## Execução

1 - Treinar o modelo utilizando Sage Maker, a partir do dataset armazenado no Dynamodb, conforme instruções a seguir, e fazer o salvamento do modelo para o S3.

2 - Criar um ambiente Docker no AWS Elastic Beanstalk.

3 - Desenvolver um serviço em python (API), utilizando algum framework http (Flask, FastApi...), que deve carregar o modelo treinado do S3 e expor um endpoint para realizar a inferência, que deverá ter logs armazenados no Dynamodb. O enpoint deve ser um POST com uma rota /api/v1/predict e receber um JSON no corpo da requisição seguindo o exemplo:

```json
{
    "no_of_adults": 3,
    "no_of_children": 3,
    "type_of_meal_plan": "example"
    ...
}
```

A resposta deve seguir este formato:

```json
{
  "result": 1
}
```

4 - Realizar o Deploy do serviço no Elastic Beanstalk.

![Esquema mostrando a cloud aws com usuários acessando api gateway esta recebendo o modelo do bucket s3 e enviando logs para dynamodb. Sagemaker ligado ao bucket para fornecer o modelo e ao dynamodb para ler e atualizar o dataset.](assets/sprint4-5.jpg)

***

## Construção do Modelo

O Hotel Reservations Dataset (<https://www.kaggle.com/datasets/ahsan81/hotel-reservations-classification-dataset>) é uma base de dados que trata de informações sobre reservas em hotéis.

Iremos utilizar esse dataset para classificar os dados por faixa de preços de acordo com as informações encontradas em suas colunas (usem o que vocês acharem que faz sentido para análise).

**Queremos saber como cada reserva (cada linha do dataset) se encaixa em qual faixa de preço.** Para isso, a equipe **deve criar uma nova coluna** chamada **label_avg_price_per_room**, que servirá como label para nossa classificação. Essa nova coluna deverá conter número 1 quando a coluna *avg_price_per_room* tiver valor menor ou igual a 85, número 2 quando a coluna *avg_price_per_room* tiver valor maior que 85 e menor que 115 e o valor 3 se a coluna *avg_price_per_room* tiver valor maior ou igual a 115.

Vocês devem então **excluir a coluna avg_price_per_room** e criar um modelo que consiga classificar os dados com base na nova coluna *label_avg_price_per_room*.

Armazene o dataset original e alterado no Dynamodb. O modelo treinado deverá ser armazenado no S3.

Será necessário explicar o porquê da escolha do modelo, como ele funciona. Também será avaliada a taxa de assertividade do modelo.

![Fluxograma para ilustração da descrição do tratamento do modelo.](assets/dataset_schema.png)

***

## O que será avaliado

- Projeto em produção na AWS Elastic Beanstalk;
- Código Python utilizado no Sagemaker (notebook python);
- Código Python usado na infererência (API);
- Código do Dockerfile e/ou docker-compose;
- Sobre o modelo:
  - Divisão dos dados para treino e teste;
  - Taxa de assertividade aceitável (se o modelo está classificando corretamente);
  - Entendimento da equipe sobre o modelo utilizado (saber explicar o que foi feito);
  - Mostrar resposta do modelo para classificação;
- Organização geral do código fonte:
  - Estrutura de pastas;
  - Divisão de responsabilidades em arquivos/pastas distintos;
  - Otimização do código fonte (evitar duplicações de código);
- Objetividade do README.md.

***

## Entrega

- **O trabalho deve ser feito em grupos de três ou quatro pessoas**;
  - **Evitar repetições de grupos de sprints anteriores**;
- Criar uma branch no repositório com o formato grupo-número (Exemplo: grupo-1);
- Subir o trabalho na branch com um README.md:
  - documentar detalhes sobre como a avaliação foi desenvolvida;
  - relatar dificuldades conhecidas;
  - descrever como utilizar o sistema;
- 🔨 Disponibilizar o código fonte desenvolvido (Sugestão: pasta `src`);
- O prazo de entrega é até às 9h do dia 27/05/2024 no repositório do github (https://github.com/Compass-pb-aws-2024-MARCO/sprints-4-5-pb-aws-marco).
