import fitz
import pandas as pd

def switch(argument):
    switcher = {
        1: "Course Title",
        2: "Cr.Hrs",
        3: "Grade",
        4: "GP",
        5: "Semester"
    }
    return switcher.get(argument, "Invalid input")

def increment(header, semester_count):
    if header == "Course":
        semester_count += 1
    return semester_count

def extract_data_from_pdf(pdf_path, csv_output_path):
    # Initialize empty list to store data
    data_list = []

    doc = fitz.open(pdf_path)
    varCount = 0
    Semester_Count = 0
    table_count = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        tables = page.find_tables()

        for table_index, table in enumerate(tables):
            table_data = table.extract()
            table_count += 1

            headers = table_data[0]
            if (varCount < 1):
                varCount += 1
                for col_index, header in enumerate(headers):
                    print(f" Column {col_index + 1}: {header}")
                print(f" Column 5: Semester")

            for col_index, header in enumerate(headers):
                Semester_Count = increment(header, Semester_Count)

            for row_index, row in enumerate(table_data[1:]):
                # Create dictionary for each row
                row_dict = {}
                for col_index, cell_text in enumerate(row):
                    row_dict[switch(col_index + 1)] = cell_text
                row_dict["Semester"] = Semester_Count
                # Append row dictionary to data list
                data_list.append(row_dict)

    # Create DataFrame from list of dictionaries
    df = pd.DataFrame(data_list)

    # Save DataFrame to CSV
    df.to_csv(csv_output_path, index=False)
    print(f"Data saved to {csv_output_path}")

def normalize_titles(df):
    df["Course Title"] = df["Course Title"].str.replace(r"\bLaboratory\b", "Lab", regex=True)
    df["Course Title"] = df["Course Title"].str.replace(r"\bLab\b", "Lab", regex=True)
    df["Course Title"] = df["Course Title"].str.replace("&", "and")
    return df

def merge_datasets(dataset1, dataset2, key='Course Title'):
    merged_df = pd.merge(dataset1, dataset2, on=key, how='inner')
    return merged_df

def has_completed_prereqs(prereqs, completed_courses):
    if prereqs == '-':
        return True
    prereq_list = [prereq.strip() for prereq in prereqs.split(',')]
    return all(prereq in completed_courses for prereq in prereq_list)