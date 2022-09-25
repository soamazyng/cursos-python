import os


def handler(event, context):

    message = 'Hello {} {}!'.format(event['first_name'], event['last_name'])

    env_var = os.getenv('ENV_VAR_TEST')

    return {
        'statusCode': 200,
        'message': 'Hello fro Python Lambda Function! {} - {}'.format(env_var, message)
    }
