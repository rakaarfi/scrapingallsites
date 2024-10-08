from datetime import datetime

# Main function to create the dictionary
def create_dict(resource, count, data):
    # Generate current time
    generated_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create the dictionary
    result = {
        "Status Code": 200,
        "Message": "OK",
        "Resource": resource,
        "Count": count,
        "Generated Time": generated_time,
        "Data": data
    }

    return result