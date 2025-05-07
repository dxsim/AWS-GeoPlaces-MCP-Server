from mcp.server.fastmcp import FastMCP
import json
import boto3
import os
'''
Client Location V2: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html
geocoding: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/geocode.html
reverse-geocoding: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/reverse_geocode.html
'''
# Get the AWS region from the environment variable
aws_region = os.environ.get('AWS_REGION')

# Create the client using the region from the environment variable
location_client = boto3.client('geo-places', region_name=aws_region)

# Create an MCP server
mcp = FastMCP("AWS-GeoPlaces-MCP-Server")

@mcp.tool()
def geocoding(query:str)->list:
    # Perform geocoding
    try:
        response = location_client.geocode(
            QueryText=query,
            IntendedUse='SingleUse'
        )
        
        results = response.get('ResultItems', [])
        return results
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

@mcp.tool()
def reverse_geocoding(longitude:float, latitude:float )->list:
    # Perform geocoding
    try:
        response = location_client.reverse_geocode(
            QueryPosition=[longitude,latitude],
            QueryRadius = 50,
            IntendedUse='SingleUse'
        )
        # Filter={'IncludeCountries': ['MY']} Included countries doesnt work
        results = response.get('ResultItems', [])
        return results
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
