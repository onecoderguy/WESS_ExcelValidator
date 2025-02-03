import pandas as pd
import json
from typing import List
from io import BytesIO
import base64

class ExcelValidator:
    def __init__(self, file_stream: BytesIO, required_headers: List[str], unique_column: str):
        self.file_stream = file_stream
        self.required_headers = required_headers
        self.unique_column = unique_column
        self.df = None
        self.errors = []
    
    def load_data(self):
        self.df = pd.read_excel(self.file_stream)
    
    def validate_headers(self):
        if list(self.df.columns) != self.required_headers:
            self.errors.append("Incorrect or unordered headers.")
    
    def validate_unique_column(self):
        if self.df[self.unique_column].duplicated().any():
            self.errors.append(f"The column '{self.unique_column}' has duplicated values.")
    
    def validate_no_empty_cells(self):
        if self.df.isnull().values.any():
            self.errors.append("Found empty cells.")
    
    def validate(self):
        self.load_data()
        self.validate_headers()
        self.validate_unique_column()
        self.validate_no_empty_cells()
        
        if self.errors:
            return {"status": "error", "errors": self.errors}
        return {"status": "success", "message": "The health of excel file is OK."}

def lambda_handler(event, context):
    try:
        # Parsing Excel file into base64 (Its necessary to sends in JSON to Lambda)
        file_content = base64.b64decode(event["file_base64"])
        file_stream = BytesIO(file_content)
        
        required_headers = [
            "Funder Hierarchy",
            "Responsible Unit Name",
            "Project Definition",
            "PD Description",
            ""
            ]  # Define desired headers
        unique_column = "Project Definition"  # The column that must be unique value
        
        validator = ExcelValidator(file_stream, required_headers, unique_column)
        response = validator.validate()
        
        return {
            "statusCode": 200 if response["status"] == "success" else 400,
            "body": json.dumps(response)
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"status": "error", "message": str(e)})
        }