import boto3

def clear_all_tables():
response = table.scan(
	FilterExpression=Attr('id').gte(0)
)