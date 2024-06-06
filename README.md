# Final Project: RMT-030 Group 001
   ![Laibrarian](https://github.com/FTDS-assignment-bay/p2-final-project-laibrarian/blob/main/deployment/lai.png)

## Members:
- Dendy Dwinanda, as Data Engineer
- Arif Imam Fauzi, as Data Engineer
- Andryan Kalmer Wijaya, as Data Engineer
- Ferrasta Sebastian Veron, as Data Scientist
- Amelia Puspita Sari, as Data Analyst


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
- Model Development: Created a recomenndation model to make product prediction based on similiarity and filter using cleaned data.
- Model Optimization: Tune and optimalize text preprocessing by make miss input correction etc.
### Data Analysis
- Visualization: Created visual representations to simplify complex information, making it more accessible.
- Reporting: Create a comprehensive report using your collected findings and insights.


## Results
- Model deployment on [Streamlit](https://laibrarian.streamlit.app)
- Exploratory Data Analysis in [tableau](https://public.tableau.com/views/DashboardBooks_FinalProject/Dashboard1?:language=en-US&:sid=&:display_count=n&:origin=viz_share_link)


