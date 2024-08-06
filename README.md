# Elective Course Recommendation System

This project is a web-based application designed to recommend elective courses to students based on their current grade report. The application uses data extraction from PDF grade reports, data processing, and a recommendation algorithm to suggest the most suitable elective courses. Built using Python and Flask, this project incorporates various data science techniques to analyze and recommend courses that align with the student's interests, career goals, and academic performance.

[![course-recommendation-system](https://github.com/user-attachments/assets/9371367c-d25f-4fcc-baa7-afa151b45cdb)]


## Features

- **Upload Grade Report:** Users can upload their PDF grade report, which is then processed to extract relevant academic data.
- **Course Recommendations:** Based on the extracted data and the predefined curriculum, the system recommends elective courses that match the student's profile.
- **Model Improvement:** Users can provide feedback to improve the recommendation model, making it more accurate over time.
- **Session Management:** The application uses session management to handle user interactions and data updates securely.

## Technical Details

### Backend

- **Flask:** The web framework used to create the application.
- **Pandas:** Used for data manipulation and analysis.
- **Fitz (PyMuPDF):** Used for extracting data from PDF files.
- **Seaborn & Matplotlib:** Used for data visualization (if necessary).

### Recommendation Algorithm

- **Data Extraction:** Extracts course titles, credits, grades, and other relevant information from the uploaded PDF grade report.
- **Data Normalization:** Normalizes course titles and merges datasets to create a comprehensive grade report.
- **Prerequisite Check:** Ensures the student has completed the necessary prerequisites for the recommended elective courses.
- **Attribute Filtering:** Filters courses based on attributes such as interest level, relevance to career goals, course popularity, project-based learning, and industry relevance.
- **Weighted Scoring:** Calculates similarity scores for elective courses using a weighted formula and recommends the top courses.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/elective-course-recommendation-system.git
   cd elective-course-recommendation-system
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   flask run
   ```

4. Access the application in your web browser at `http://127.0.0.1:5000`.

## Usage

1. **Home Page:** Start by uploading your PDF grade report.
2. **Recommendations:** View the recommended elective courses based on your current academic profile.
3. **Improve Model:** Provide feedback to improve the recommendation model.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

---
