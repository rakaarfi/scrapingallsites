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

# Dictionary to show categories and link from each source
def generate_result(links_data, categories):
    result = {}
    # Looping each source(detik, kompas and tribun)
    # Data is categories and its link
    for source, data in links_data.items():
        source_categories = []
        # Categories is list of categories
        for category in categories:
            # If there is a category, get the link
            # If not, None
            source_categories.append({category: data.get(category, None)})
        result[source] = {'categories': source_categories}
    return result