import base64
import json
import argparse
from io import BytesIO
from WESS_ExcelValidator import lambda_handler

def main():
    parser = argparse.ArgumentParser(description="Test excel file validate to Lambda.")
    parser.add_argument("file_path", type=str, help="Path from excel file to test.")
    args = parser.parse_args()

    try:
        with open(args.file_path, "rb") as file:
            file_base64 = base64.b64encode(file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: The file '{args.file_path}' not found in path.")
        return

    # Simulate lambda event
    event = {"file_base64": file_base64}
    context = {}  #TODO: Need to update to context from AWS environment

    # Call lambda_handler locally
    response = lambda_handler(event, context)

    # Show formatted result
    print(json.dumps(json.loads(response["body"]), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
