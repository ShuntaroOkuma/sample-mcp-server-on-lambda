# AWS Lambdaの公式Python 3.12イメージをベースとして使用
FROM public.ecr.aws/lambda/python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY src/ ${LAMBDA_TASK_ROOT}/src

# CMDはtemplate.yamlで指定するため、ここでは設定しない
