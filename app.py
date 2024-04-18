from flask import Flask, request, jsonify, send_file
import pandas as pd
import io

app = Flask(__name__)

@app.route('/merge_excel_columns', methods=['POST'])
def merge_excel_columns():
    try:
        # Get the input Excel file from the POST request
        input_file = request.files['file']
        
        # Read the Excel file
        df = pd.read_excel(input_file)
        
        # Initialize an empty dictionary to store merged columns
        merged_columns = {}
        
        # Iterate over columns
        for col in df.columns:
            # Extract the header name
            header_name = col.split('.')[0]
            
            # Check if the header name already exists in the merged_columns dictionary
            if header_name in merged_columns:
                # If it exists, merge the columns
                merged_columns[header_name] = merged_columns[header_name].fillna(df[col])
            else:
                # If it doesn't exist, add it to the dictionary
                merged_columns[header_name] = df[col]
        
        # Create a new DataFrame from the merged columns dictionary
        merged_df = pd.DataFrame(merged_columns)
        
        # Convert the merged DataFrame to an Excel file in memory
        output_file = io.BytesIO()
        merged_df.to_excel(output_file, index=False)
        output_file.seek(0)
        
        # Return the merged Excel file as a response
        return send_file(output_file, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, attachment_filename='output.xlsx')
    except Exception as e:
        # Return an error message if an exception occurs
        return jsonify({'error': str(e)})

@app.route('/hello')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()
