import boto3
import json, typing
from os import path

from src.utils import Utils

LAMBDA_ACCESS_POLICY_ARN = 'arn:aws:iam::712790115760:policy/LambdaS3AccessPolicy'
LAMBDA_ROLE = 'Lambda_Execution_Role'
LAMBDA_ROLE_ARN = 'arn:aws:iam::712790115760:role/Lambda_Execution_Role'
LAMBDA_TIMEOUT = 10
LAMBDA_MEMORY = 128
PYTHON_39_RUNTIME = 'python3.9'
PYTHON_LAMBDA_NAME = 'Python_Lambda_Function'
NODEJS_LAMBDA_NAME = 'NodeJS_Lambda_Function'
LAMBDA_HANDLER = "lambda_function.handler"
NODEJS_16_RUNTIME = "nodejs16.x"


def lambda_client():
    aws_lambda = boto3.client('lambda', region_name='us-east-1')
    """:type : pyboto3.lamda"""
    return aws_lambda


def iam_client():
    iam = boto3.client("iam")
    """ :type : pyboto3.lambda """
    return iam


def create_access_policy_for_lambda():
    s3_access_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "s3:*",
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Effect": "Allow",
                "Resource": "*"
            }
        ]
    }

    return iam_client().create_policy(
        PolicyName='LambdaS3AccessPolicy',
        PolicyDocument=json.dumps(s3_access_policy_document),
        Description='Allows lambda function to access s3 resources'
    )


def create_execution_role_for_lambda():
    lambda_execution_assumption_role = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    return iam_client().create_role(
        RoleName=LAMBDA_ROLE,
        AssumeRolePolicyDocument=json.dumps(lambda_execution_assumption_role),
        Description="Gives necessary permissions for lambda to be executed"
    )


def attach_access_policy_to_execution_role():
    return iam_client().attach_role_policy(
        RoleName=LAMBDA_ROLE,
        PolicyArn=LAMBDA_ACCESS_POLICY_ARN
    )


def deploy_lambda_function(function_name, runtime, handler, role_arn, source_folder):
    folder_path = path.join(path.dirname(path.abspath(__file__)), source_folder)
    zip_file = Utils.make_zip_file_bytes(path=folder_path)

    return lambda_client().create_function(
        FunctionName=function_name,
        Runtime=runtime,
        Role=role_arn,
        Handler=handler,
        Code={
            'ZipFile': zip_file
        },
        Timeout=LAMBDA_TIMEOUT,
        MemorySize=LAMBDA_MEMORY,
        Publish=False
    )


def invoke_lambda_function(function_name, payload:typing.Mapping[str, str]=None):

    return lambda_client().invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload))


def add_environment_variables_to_lambda(function_name, variables):

    return lambda_client().update_function_configuration(
        FunctionName=function_name,
        Environment=variables
    )


def update_lambda_function_code(function_name, source_folder):

    folder_path = path.join(path.dirname(path.abspath(__file__)), source_folder)
    zip_file = Utils.make_zip_file_bytes(path=folder_path)

    return lambda_client().update_function_code(
        FunctionName=function_name,
        ZipFile=zip_file
    )


def publish_a_new_version(function_name):
    return lambda_client().publish_version(
        FunctionName=function_name)


def create_alias_for_new_version(function_name, alias_name, version):
    return lambda_client().create_alias(
        FunctionName=function_name,
        Name=alias_name,
        FunctionVersion=version,
        Description="This is the {} alias for function".format(alias_name)
    )


def invoke_labmda_with_alias(function_name, payload, alias_name):
    return lambda_client().invoke(
        FunctionName=function_name,
        Qualifier=alias_name,
        Payload=json.dumps(payload)
    )


if __name__ == '__main__':

    # print(create_access_policy_for_lambda())
    # print(create_execution_role_for_lambda())
    # print(attach_access_policy_to_execution_role())
    # print(deploy_lambda_function(NODEJS_LAMBDA_NAME, NODEJS_16_RUNTIME, LAMBDA_HANDLER, LAMBDA_ROLE_ARN, 'nodejs_lambda'))

    # payload = {
    #     "first_name": "Jaqueline",
    #     "last_name": "Benedicto"
    # }
    #
    # response = invoke_lambda_function(PYTHON_LAMBDA_NAME, payload)
    # print(response['Payload'].read().decode())
    # env_variables = {
    #     'Variables': {
    #         'ENV_VAR_TEST': 'This is an environment variable!'
    #     }
    # }
    # add_environment_variables_to_lambda(PYTHON_LAMBDA_NAME, env_variables)
    # print(update_lambda_function_code(PYTHON_LAMBDA_NAME, 'python_lambda'))
    # print(publish_a_new_version(PYTHON_LAMBDA_NAME))
    # print(create_alias_for_new_version(PYTHON_LAMBDA_NAME, "PROD", '1'))

    payload = {
        "first_name": "Jaqueline",
        "last_name": "Benedicto"
    }

    response = invoke_labmda_with_alias(PYTHON_LAMBDA_NAME, payload, 'PROD')
    print(response['Payload'].read().decode())

