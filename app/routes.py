from flask import render_template, request, redirect, url_for, flash, session
import pandas as pd
from app import app
from recommendation_system import run_recommendation_system

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    pdf_file.save(r'C:\Users\HP\Documents\Projects\DS Semester Project\Yasir efforts\with flask\uploads\Grade Report.pdf')  # Save the uploaded PDF
    return redirect(url_for('recommendations'))

@app.route('/recommendations')
def recommendations():
    try:
        grade_report_path = r'C:\Users\HP\Documents\Projects\DS Semester Project\Yasir efforts\with flask\uploads\Grade Report.pdf'
        curriculum_path = r'C:\Users\HP\Documents\Projects\DS Semester Project\Yasir efforts\with flask\refined_data.csv'
        electives_path = r'C:\Users\HP\Documents\Projects\DS Semester Project\Yasir efforts\with flask\refined_data.csv'

        recommendations = run_recommendation_system(grade_report_path, curriculum_path, electives_path)

        return render_template('recommendations.html', recommendations=recommendations.to_dict('records'))
    except Exception as e:
        return render_template('recommendations.html', recommendations=[], error=str(e))

csv_file_path = r'C:\Users\HP\Documents\Projects\DS Semester Project\Yasir efforts\refined_data.csv'

@app.route('/improve_model', methods=['GET', 'POST'])
def improve_model():
    if 'submission_count' not in session:
        session['submission_count'] = 0

    if request.method == 'POST':
        # Get updated data from form submission
        updated_data = request.form.to_dict(flat=False)
        
        # Convert updated data into a DataFrame
        df = pd.read_csv(csv_file_path)
        
        for col in updated_data.keys():
            if col not in df.columns:
                continue

            user_input = updated_data[col][0]
            submission_count = session['submission_count']
            percentage_change = 0.05 / (1 + submission_count * 0.5)

            # Handle Skillset Covered by concatenating new skills if they aren't present
            if col == 'Skillset Covered':
                df[col] = df[col].apply(lambda x: x + ', ' + user_input if pd.notnull(x) and user_input not in x.split(', ') else x)
            else:
                # Convert numeric columns to numeric type
                if pd.api.types.is_numeric_dtype(df[col]):
                    try:
                        user_input_value = float(user_input)
                        df[col] = df[col].apply(lambda x: x + (user_input_value - x) * percentage_change if pd.notnull(x) else x)
                    except ValueError:
                        continue  # Skip non-numeric columns
        
        # Save updated DataFrame back to CSV with explicit numeric data types
        df.to_csv(csv_file_path, index=False, float_format='%.2f')

        session['submission_count'] += 1
        flash('Model data updated successfully!')
        return redirect(url_for('improve_model'))

    # Read the existing CSV data
    df = pd.read_csv(csv_file_path)
    
    # Columns to exclude from display
    exclude_columns = ['Sr.', 'Pre-req', 'Semester', 'Course Difficulty Level', 'Project-Based Learning']
    
    # Filter out the columns to exclude
    columns = [col for col in df.columns if col not in exclude_columns]

    # Move the Course Title column to the first position
    if 'Course Title' in columns:
        columns.remove('Course Title')
        columns.insert(0, 'Course Title')

    data_dict = df[columns].to_dict('records')

    return render_template('improve_model.html', data=data_dict, columns=columns)
