# Reddit Sentiment Analysis Tool

This tool analyzes sentiment from Reddit posts in a specified subreddit using natural language processing models. The analysis results can be saved in CSV or Excel format, and you can optionally visualize the results.

## Setup Instructions

### 1. Create a Virtual Environment

Start by creating a Python virtual environment named `.venv`:

`python -m venv .venv`

### 2. Activate the Virtual Environment

Activate the virtual environment you created:

- **On Windows:**

  `.venv\Scripts\activate`

- **On macOS/Linux:**

  `source .venv/bin/activate`

### 3. Set Up Reddit API Credentials

To use this tool, you need to provide Reddit API credentials. You can do this in one of the following ways:

- **Option 1: Export Environment Variables**

  In your terminal, export the necessary environment variables:

  ```
  export REDDIT_CLIENT_ID=your_reddit_client_id
  export REDDIT_CLIENT_SECRET=your_reddit_client_secret
  ```

- **Option 2: Create a .env File**

  Alternatively, you can create a `.env` file in the root directory of this repository and add your credentials:
```
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
```

### 4. Install the Package

Once the environment is set up and activated, install the package in editable mode:

`pip install -e .`

### 5. Run the CLI Tool

You can now run the CLI tool with the required and optional flags:

`sentiment-analysis --subreddit <subreddit_name> [--confidence_threshold <threshold>] [--visualize] [--report <csv|excel>]`

- **--subreddit (required):** Specify the subreddit to analyze.  
- **--confidence_threshold (optional):** Set the confidence threshold for sentiment filtering (default: 0.75).  
- **--visualize (optional):** Enable visualization of sentiment analysis results.  
- **--report (optional):** Specify the report format (csv or excel). If not provided, no report will be generated.

### Example Usage

Analyze the "python" subreddit with a confidence threshold of 0.8, generate a report in Excel format, and visualize the results:

`sentiment-analysis --subreddit python --confidence_threshold 0.8 --report excel --visualize`
