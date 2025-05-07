from mcp.server.fastmcp import FastMCP
import json
import boto3
import os
from dotenv import load_dotenv
'''
Client Location V2: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places.html
geocoding: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/geocode.html
reverse-geocoding: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-places/client/reverse_geocode.html
'''
# Load environment variables from .env file
load_dotenv()

# Get the AWS region from the environment variable
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')

# Create the boto3 client
location_client = boto3.client('geo-places', 
                               region_name=aws_region,
                               aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key)
# Create an MCP server
mcp = FastMCP("AWS-GeoPlaces-MCP-Server")

@mcp.tool()
def geocoding(query: str) -> list:
    """
    Perform geocoding to convert a text-based location query into geographic coordinates.

    This function takes a string representing an address, place name, or point of interest
    and returns a list of possible geographic coordinate matches. It uses a geocoding service
    to convert the text-based query into one or more sets of latitude and longitude coordinates.

    Args:
        query (str): A string representing the location to geocode. This can be an address
                     (e.g., "1600 Amphitheatre Parkway, Mountain View, CA"), a place name
                     (e.g., "Eiffel Tower"), or any other location descriptor that the
                     geocoding service can interpret.
    Returns:
        list: List of responses return by geoplaces api.
    """
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
def reverse_geocoding(longitude: float, latitude: float, radius: float) -> list:
    """
    Perform reverse geocoding to convert geographic coordinates to a human-readable address.

    This function takes a pair of geographic coordinates (longitude and latitude) and returns
    a list of possible address matches for that location. The function uses a reverse geocoding
    service to convert the coordinates into one or more human-readable addresses.
    
    [DD (decimal degree) Coordinates only: ie 1.483998064 110.341331968]

    Args:
        longitude (float): The longitude coordinate of the location. 
                           Must be a float value between -180 and 180.
        latitude (float): The latitude coordinate of the location. 
                          Must be a float value between -90 and 90.
        latitude (float): The maximum distance in meters from the QueryPosition 
                            from which a result will be returned.
                          
    Returns:
        list: List of responses return by geoplaces api.
    """
    try:
        response = location_client.reverse_geocode(
            QueryPosition=[longitude,latitude],
            QueryRadius = radius,
            IntendedUse='SingleUse'
        )
        results = response.get('ResultItems', [])
        return results
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
