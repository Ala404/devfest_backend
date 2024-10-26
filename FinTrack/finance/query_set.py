from fastapi import FastAPI,HTTPException
import re
from transformers import BertForSequenceClassification,AutoTokenizer,Trainer,BartTokenizer, BartForConditionalGeneration
import torch
import requests
import json
import base64
import io
from pydantic import BaseModel
import spacy
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import torch
import spacy
import pandas as pd
from transformers import BertForSequenceClassification, AutoTokenizer, Trainer
from sklearn.preprocessing import LabelEncoder
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .serializers import *
import google.generativeai as genai
GOOGLE_API_KEY = 'AIzaSyCl1UpKx-JDl09jv20NrzpnR1yJBXE3nco'
genai.configure(api_key=GOOGLE_API_KEY)

model_generation = genai.GenerativeModel("gemini-1.5-flash")
import google.generativeai as genai
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM



# # Load NLP and model components
nlp = spacy.load("en_core_web_sm")
df = pd.read_csv("finance/tttt.txt", header=None, names=["text", "target"])
label_encoder = LabelEncoder()
df["target"] = label_encoder.fit_transform(df["target"])
DarijaBert_model = BertForSequenceClassification.from_pretrained('finance/model')
DarijaBERT_tokenizer = AutoTokenizer.from_pretrained('finance/model')
trainer = Trainer(model=DarijaBert_model)
device = torch.device("cpu")
DarijaBert_model.to(device)


model = AutoModelForSeq2SeqLM.from_pretrained("finance/model_sql")
tokenizer = AutoTokenizer.from_pretrained("finance/model_sql")
# Define Dataset class for the model
class CoherenceDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels=None):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        if self.labels is not None:
            item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.encodings["input_ids"])

class requestAnalyst(GenericAPIView):
    serializer_class = TextInputSerializer  # Specify the serializer

    def post(self, request, *args, **kwargs):
        # Validate and retrieve the input text using the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        input_text = serializer.validated_data["text"]

        # Tokenize the input text
        doc = nlp(input_text)
        test_encodings = DarijaBERT_tokenizer(
            [sent.text for sent in doc.sents],
            truncation=True,
            padding=True,
            max_length=256
        )

        # Prepare the dataset for prediction
        test_dataset = CoherenceDataset(test_encodings, labels=None)

        # Make predictions
        predictions = trainer.predict(test_dataset)
        probabilities = torch.nn.functional.softmax(torch.from_numpy(predictions.predictions), dim=-1)
        predicted_labels = torch.argmax(probabilities, dim=1)
        coherent = predicted_labels.tolist()

        # Process label encoding
        try:
            decoded_labels = label_encoder.inverse_transform(coherent)
            table_script=get_table_creation_script(input_text)
            sql_query_result=generate_sql_query(input_text,table_script,model,tokenizer)
            result_sql_geminie = model_generation.generate_content([
                "sql query: " + sql_query_result,
                # "\n",
                # "the prompt: " + input_text,
                # "sql context: " + table_script,
                "\n\n",
                "Correct this SQL query based on the provided information and return only the SQL query."
            ])


        except FileNotFoundError:
            return Response({"error": "Label file not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        a = decoded_labels.tolist()
        answers = []
        for i in a:
            if i =='cashflow':
                pass
            if i in ['costume_dashboard_help', 'costume_dashboard_help_help']:
                result_custom = model_generation.generate_content([input_text, "\n\n", "answer this as a fianace platform assistance "]) #  Promp
                answers.append(result_custom)
            if i == 'expences':
                pass
            if i == 'financial_report_help':
                financial_report = model_generation.generate_content([input_text, "\n\n", "answer this as a finance platform assistance"])
                answers.append(financial_report)
            if i == "find_expences_tracking":
                expences_tracking = model_generation.generate_content([input_text, "\n\n", "answer this as a finance platform assistance"])
                answers.append(expences_tracking)
            if i == "insert":
                pass
            if i == "profile_pics":
                pass # TODO WALID
            if i == "profit_prediction":
                pass # requet sql
            if i == "upload_file_analysis_help":
                upload_file = model_generation.generate_content([input_text, "\n\n", "answer this as a finance platform assistance"])
                answers.append(upload_file)


        # Return the decoded labels as the response
        return Response({
            # "predicted_labels": decoded_labels.tolist(),
            "sql_query":sql_query_result
        })
    




# Import necessary libraries (if any additional needed, e.g., tokenizer setup)
# Define a dictionary mapping table names to their creation scripts
table_creation_scripts = {
    "cashflow": """
CREATE TABLE CashFlow (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    cash_inflow DECIMAL(15, 2) NOT NULL,
    cash_outflow DECIMAL(15, 2) NOT NULL,
    net_cash_flow DECIMAL(15, 2) NOT NULL,
    description TEXT,
    category VARCHAR(50)
);
""",
    "expenses": """
CREATE TABLE Expenses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    expense_category VARCHAR(50),
    department VARCHAR(50),
    description TEXT
);
""",
    "revenue": """
CREATE TABLE Revenue (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    product_line VARCHAR(50),
    customer_type VARCHAR(50),
    description TEXT
);
""",
    "profit": """
CREATE TABLE Profit (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    revenue DECIMAL(15, 2) NOT NULL,
    expenses DECIMAL(15, 2) NOT NULL,
    net_profit DECIMAL(15, 2) NOT NULL,
    profit_margin DECIMAL(5, 2),
    description TEXT
);
""",
    "budget": """
CREATE TABLE Budget (
    id INT PRIMARY KEY AUTO_INCREMENT,
    fiscal_year VARCHAR(50),
    department VARCHAR(50),
    allocated_budget DECIMAL(15, 2) NOT NULL,
    spent_budget DECIMAL(15, 2) NOT NULL,
    remaining_budget DECIMAL(15, 2) NOT NULL,
    description TEXT
);
""",
    "debt": """
CREATE TABLE Debt (
    id INT PRIMARY KEY AUTO_INCREMENT,
    debt_type VARCHAR(50),
    principal DECIMAL(15, 2) NOT NULL,
    interest_rate DECIMAL(5, 2),
    maturity_date DATE,
    payment_due_date DATE,
    amount_paid DECIMAL(15, 2),
    outstanding_balance DECIMAL(15, 2),
    description TEXT
);
""",
    "investments": """
CREATE TABLE Investments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    investment_type VARCHAR(50),
    investment_amount DECIMAL(15, 2) NOT NULL,
    investment_date DATE NOT NULL,
    returns DECIMAL(15, 2),
    risk_level VARCHAR(50),
    current_value DECIMAL(15, 2),
    description TEXT
);
""",
    "funding": """
CREATE TABLE Funding (
    id INT PRIMARY KEY AUTO_INCREMENT,
    funding_round VARCHAR(50),
    amount_raised DECIMAL(15, 2) NOT NULL,
    date DATE NOT NULL,
    investor_name VARCHAR(50),
    valuation DECIMAL(15, 2),
    description TEXT
);
""",
    "financialreports": """
CREATE TABLE FinancialReports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_type VARCHAR(50),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""",
    "assetsliabilities": """
CREATE TABLE AssetsLiabilities (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asset_name VARCHAR(50),
    asset_value DECIMAL(15, 2),
    liability_name VARCHAR(50),
    liability_value DECIMAL(15, 2),
    date DATE NOT NULL,
    description TEXT
);
"""
}

def get_table_creation_script(prompt):
    # Convert prompt to lowercase for case-insensitive search
    prompt_lower = prompt.lower()
    
    # Search for any table name in the prompt
    for table_name, script in table_creation_scripts.items():
        if table_name in prompt_lower:
            return f"Table '{table_name.capitalize()}' found. Here is the creation script:\n{script}"
    
    # If no table name is found

    return "No matching table name found in the prompt."

def generate_sql_query(prompt,sql_context, model,tokenizer, max_new_tokens=100):

    # Get the SQL context by retrieving the table creation script
    # sql_context = get_table_creation_script(prompt)
    if "No matching table name found" in sql_context:
        raise ValueError("Table not found in schema.")

    # Prepare the query question with SQL context
    query_question_with_context = f"sql_prompt: {prompt}\nsql_context: {sql_context}"

    # # Load the model and tokenizer
    # model = AutoModelForSeq2SeqLM.from_pretrained(model)
    # tokenizer = AutoTokenizer.from_pretrained(model)

    # Tokenize and generate the SQL query
    inputs = tokenizer(query_question_with_context, return_tensors="pt").input_ids
    outputs = model.generate(inputs, max_new_tokens=max_new_tokens, do_sample=False)

    # Decode the output
    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return sql_query



# # Example usage
# prompt = "What is the structure of the Revenue table?"
# creation_script = get_table_creation_script(prompt)
# print(creation_script)

# query_question_with_context = """sql_prompt: show max amount ?
# sql_context: CREATE TABLE Revenue (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     date DATE NOT NULL,
#     amount DECIMAL(15, 2) NOT NULL,
#     product_line VARCHAR(50),
#     customer_type VARCHAR(50),
#     description TEXT
# );"""

# inputs = tokenizer(query_question_with_context, return_tensors="pt").input_ids
# outputs = model.generate(inputs, max_new_tokens=100, do_sample=False)

# sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
# print(sql)
