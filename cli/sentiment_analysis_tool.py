import os
import click
import praw
import pandas as pd
from transformers import pipeline
from pprint import pprint
import matplotlib.pyplot as plt
import seaborn as sns
import torch
from dotenv import load_dotenv
from datetime import datetime
import warnings

# Set constants and configurations
load_dotenv()
DEVICE = 0 if torch.cuda.is_available() else -1
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
USER_AGENT_DESC = "Sentiment Analyzer 1.0"
warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

# Entrypoint function to read CLI input
def cli_entrypoint():
    """Reads and returns the CLI input."""
    @click.command()
    @click.option('--subreddit', required=True, help='Subreddit to analyze.')
    @click.option('--confidence_threshold', default=0.75, help='Confidence threshold for sentiment filtering.')
    @click.option('--visualize', is_flag=True, help='Enable visualization of sentiment analysis results.')
    @click.option('--report', type=click.Choice(['csv', 'excel'], case_sensitive=False), help='Generate a report in the specified format: csv or excel.')
    def invoke_cli(subreddit, confidence_threshold, visualize, report):
        print("Processing user input...")
        cli_driver(subreddit, confidence_threshold, visualize, report)

    invoke_cli()

# Helper function to gather headlines from the specified subreddit
def gather_headlines(subreddit):
    """Fetches the headlines and URLs from the given subreddit."""
    # Initialize Reddit API client
    reddit = praw.Reddit(
        client_id=os.environ.get("REDDIT_CLIENT_ID"),
        client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
        user_agent="Sentiment Analyzer 1.0"
    )

    headlines = []
    # Fetch submissions in descending order by creation date
    for submission in reddit.subreddit(subreddit).new(limit=None):
        # Store both headline and URL
        headlines.append((submission.title, submission.url, submission.created_utc))

    # Sort headlines by creation time in descending order
    headlines.sort(key=lambda x: x[2], reverse=True)
    
    print(f"Gathered {len(headlines)} headlines from r/{subreddit}...")
    # Return only the title and URL for further processing
    return [(title, url) for title, url, _ in headlines]



# Helper function to run the sentiment analysis pipeline
def run_sentiment_analysis(headlines):
    """Runs sentiment analysis using the CardiffNLP pipeline."""
    sentiment_pipeline = pipeline(
        "sentiment-analysis", 
        model="cardiffnlp/twitter-roberta-base-sentiment", 
        device=DEVICE, 
    )

    print("Running sentiment analysis pipeline...")

    # Mapping from model labels to sentiment names
    label_to_sentiment = {
        'LABEL_0': 'negative',
        'LABEL_1': 'neutral',
        'LABEL_2': 'positive'
    }

    results = []
    for title, url in headlines:
        sentiment = sentiment_pipeline(title)  # Perform sentiment analysis
        pol_score = sentiment[0]  # Extract the first result
        pol_score['headline'] = title  # Keep headline separate
        pol_score['url'] = url  # Add URL as a new column
        pol_score['sentiment'] = label_to_sentiment[pol_score['label']]  # Map and store the sentiment class
        results.append(pol_score)

    return pd.DataFrame.from_records(results)


# Helper function to filter results by confidence threshold
def filter_by_confidence(df, confidence_threshold):
    """Filters the DataFrame based on the confidence threshold and excludes neutral sentiments."""
    print(f"Filtering headlines based on input confidence threshold of {confidence_threshold}...")
    filtered_df = df[(df['score'] >= confidence_threshold) & (df['sentiment'] != 'neutral')]
    filtered_df.drop(columns=['label'], inplace=True)
    return filtered_df


# Helper function to write the report
def write_report_csv(df, subreddit):
    """Writes a human-readable report to the reports folder."""
    # Ensure the reports directory exists
    if not os.path.exists('reports'):
        os.makedirs('reports')

    # Write to CSV file
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    report_path = os.path.join('reports', f'{subreddit}_sentiment_report_{current_time}.csv')
    df.to_csv(report_path, index=False, columns=['headline', 'sentiment', 'score', 'url'])
    print(f"Report generated at {report_path}")

# Helper function to write the report
def write_report_xlsx(df, subreddit):
    """Writes a human-readable report to the reports folder."""
    # Ensure the reports directory exists
    if not os.path.exists('reports'):
        os.makedirs('reports')

    # Write to CSV file
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    report_path = os.path.join('reports', f'{subreddit}_sentiment_report_{current_time}.xlsx')

    # Create a Pandas Excel writer using XlsxWriter as the engine
    with pd.ExcelWriter(report_path, engine='xlsxwriter') as writer:
        # Convert the DataFrame to an Excel object
        df.to_excel(writer, index=False, columns=['headline', 'sentiment', 'score', 'url'], sheet_name='Sentiment Analysis')

    print(f"Report generated at {report_path}")


# Helper function to visualize sentiment results
def visualize_results(filtered_df):
    """Visualizes the sentiment analysis results."""
    counts = (filtered_df.sentiment.value_counts(normalize=True) * 100)
    pprint("Value counts of sentiment classes:")
    pprint(counts)

    fig, ax = plt.subplots(figsize=(8, 8))
    sns.barplot(x=counts.index, y=counts, ax=ax)
    ax.set_ylabel("Percentage with confidence threshold filter")
    plt.show()


# Main function to call helper functions
def cli_driver(subreddit, confidence_threshold, visualize, report):
    """Main function to orchestrate the sentiment analysis."""
    # Step 1: Gather headlines
    headlines = gather_headlines(subreddit)

    # Step 2: Run sentiment analysis
    df = run_sentiment_analysis(headlines)

    # Step 3: Filter by confidence threshold
    filtered_df = filter_by_confidence(df, confidence_threshold)

    # Step 4: Generate report if the flag is set
    if report:
        if report == 'csv':
            write_report_csv(filtered_df, subreddit)
        elif report == 'excel':
            write_report_xlsx(filtered_df, subreddit)

    # Step 5: Visualize results if the flag is set
    if visualize:
        visualize_results(filtered_df)


if __name__ == '__main__':
    cli_entrypoint()
