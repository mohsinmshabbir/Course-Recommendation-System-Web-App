import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from data_processing import normalize_titles, merge_datasets, has_completed_prereqs, extract_data_from_pdf

def run_recommendation_system(pdf_path, curriculum_path, electives_path):
    # Extract data from PDF and save to CSV
    extract_data_from_pdf(pdf_path, "grade_report.csv")

    # Load datasets
    curriculum = pd.read_csv(curriculum_path)
    grade_report = pd.read_csv('grade_report.csv')

    # Normalize course titles
    grade_report = normalize_titles(grade_report)
    curriculum = normalize_titles(curriculum)

    # Drop unnecessary columns
    curriculum.drop(['Cr. Hrs.','Semester'], axis=1, inplace=True)
    grade_report.drop('Semester',axis=1, inplace=True)

    # Merge datasets
    complete_grade_report = merge_datasets(curriculum, grade_report)

    # Load elective courses and filter
    elective_courses = pd.read_csv(electives_path)
    elective_courses = elective_courses[elective_courses['Semester'] == '-']
    elective_courses.drop('Semester', axis=1, inplace=True)
    elective_courses['Cr. Hrs.'] = elective_courses['Cr. Hrs.'].str.split('-').str[-1]

    # Filter out already taken electives
    taken_courses = set(complete_grade_report['Course Title'])
    filtered_electives = elective_courses[~elective_courses['Course Title'].isin(taken_courses)]

    # Check prerequisites
    completed_courses = set(complete_grade_report['Course Code'])
    eligible_electives = filtered_electives[filtered_electives['Pre-req'].apply(has_completed_prereqs, completed_courses=completed_courses)]

    # Map difficulty levels
    difficulty_mapping = {
        'Easy': 1,
        'Moderate': 2,
        'Hard': 3
    }
    complete_grade_report['Course Difficulty Level'] = complete_grade_report['Course Difficulty Level'].map(difficulty_mapping)
    eligible_electives['Course Difficulty Level'] = eligible_electives['Course Difficulty Level'].map(difficulty_mapping)

    # Filter courses with GP >= 7.00
    high_gp_courses = complete_grade_report[complete_grade_report['GP'] >= 7.00]

    # # Visualize GP against various attributes
    # plt.figure(figsize=(16, 20))
    # continuous_columns = ['Interest Level', 'Relevance to Career Goals', 'Course Popularity', 'Project-Based Learning', 'Industry Relevance']
    # for i, column in enumerate(continuous_columns, 1):
    #     plt.subplot(3, 2, i)
    #     sns.scatterplot(x='GP', y=column, data=high_gp_courses)
    #     plt.title(f'GP vs {column}')
    #     plt.xlabel('GP')
    #     plt.ylabel(column)

    # plt.subplot(3, 2, 6)
    # sns.boxplot(x='Course Difficulty Level', y='GP', data=high_gp_courses)
    # plt.title('GP vs Course Difficulty Level')
    # plt.xlabel('Course Difficulty Level')
    # plt.ylabel('GP')

    # plt.tight_layout()
    # plt.show()

    # Calculate minimum values for attributes
    attributes = [
        'Course Difficulty Level', 
        'Interest Level', 
        'Relevance to Career Goals', 
        'Course Popularity', 
        'Project-Based Learning', 
        'Industry Relevance'
    ]
    min_values = high_gp_courses[attributes].min()

    # Filter eligible electives based on minimum values
    filtered_electives = eligible_electives.copy()
    for attribute in attributes:
        filtered_electives = filtered_electives[filtered_electives[attribute] >= min_values[attribute]]

    # Apply weighted formula and calculate similarity scores
    weights = {
        'Course Difficulty Level': 0.2,
        'Interest Level': 0.2,
        'Relevance to Career Goals': 0.2,
        'Course Popularity': 0.1,
        'Project-Based Learning': 0.2,
        'Industry Relevance': 0.1
    }
    filtered_electives['Similarity Score'] = 0
    for attribute in attributes:
        filtered_electives['Similarity Score'] += filtered_electives[attribute] * weights[attribute]

    # Round similarity scores to two decimal places
    filtered_electives['Similarity Score'] = filtered_electives['Similarity Score'].round(2)

    # Recommend top courses
    top_recommendations = filtered_electives.sort_values(by='Similarity Score', ascending=False)

    # Additional logic for lab courses
    recommended_courses = top_recommendations['Course Title'].tolist()
    updated_recommendations = top_recommendations.copy()

    for course in recommended_courses:
        if 'Lab' not in course:
            lab_course = course + ' Lab'
            if lab_course in eligible_electives['Course Title'].tolist():
                lab_row = eligible_electives[eligible_electives['Course Title'] == lab_course]
                updated_recommendations = pd.concat([updated_recommendations, lab_row])
        else:
            main_course = course.replace(' Lab', '')
            if main_course not in recommended_courses:
                updated_recommendations = updated_recommendations[updated_recommendations['Course Title'] != course]

    updated_recommendations = updated_recommendations.drop_duplicates(subset=['Course Title'])
    updated_recommendations = updated_recommendations.sort_values(by='Similarity Score', ascending=False)

    return updated_recommendations[['Course Title', 'Similarity Score'] + attributes]