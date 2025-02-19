from rest_framework.views import exception_handler


def format_api_error_response(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_response = {
            "status": "error",  # Default status for error handling
            "message": str(exc),  # Default message is the exception string
            "status_code": response.status_code,
            "errors": []  # List to hold any specific error details
        }

        if isinstance(response.data, dict):
            for key, value in response.data.items():
                if isinstance(value, list) and value:
                    custom_response["errors"].append({
                        "field": key,
                        "message": str(value[0])  # Taking the first error message
                    })
                else:
                    custom_response["errors"].append({
                        "field": key,
                        "message": str(value)
                    })

        custom_response["data"] = response.data if response.data else {}

        response.data = custom_response

    return response
