# Final Project: RMT-030 Group 001
   ![Laibrarian](https://github.com/FTDS-assignment-bay/p2-final-project-laibrarian/blob/main/deployment/lai.png)

## Members:
- Dendy Dwinanda, as Data Engineer
- Andryan Kalmer Wijaya, as Data Engineer
- Ferrasta Sebastian Veron, as Data Scientist
- Amelia Puspita Sari, as Data Analyst, Data Scientist
- Arif Imam Fauzi, as Data Analyst, Data Engineer


## Background
### Problem Statement
Based on the reports from the American Library Association (ALA) and surveys by the Pew Research Center on reading habits, each year shows an increasing trend where many readers rely on online recommendations and digital platforms to discover new books they want to read.

A web-based book recommendation application is an effective solution to assist users in finding books that match their preferences. By leveraging machine learning and AI, this application can provide personalized and relevant recommendations.

### Objectives
- Create machine learning model using NLP for analyzing text such as book description, author, categories, etc.
- Build a recommendation system with said model to recommend books based on user's preference and description.

### Dataset
The dataset is obtained from [Kaggle](https://www.kaggle.com/datasets/abdallahwagih/books-dataset/data).


## Workflow
### Data Engineering
- Data Collection: Store raw data on PostgreSQL
- Data Cleaning: Set up Apache Airflow DAG to automation fetch and clean raw data
- Data Storage: Store the cleaned data back into the PostgreSQL
### Data Science
- Model Development: Built a recommendation model using TF-IDF to recommend books using description.
- Model Optimization: Optimize using different parameter and correcting typos from the input.
### Data Analysis
- Visualization: Created dashboard to visualize findings on the dataset about books.
- Reporting: Created deck to report the insights and model demo.


## Results
- Model deployment on [Streamlit](https://laibrarian.streamlit.app)
- Exploratory Data Analysis in [tableau](https://public.tableau.com/views/DashboardBooks_FinalProject/Dashboard1?:language=en-US&:sid=&:display_count=n&:origin=viz_share_link)


