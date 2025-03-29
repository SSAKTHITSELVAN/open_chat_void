# README.md
# Message Search App

A lightweight messaging system with full-text search capabilities built with Streamlit, Python, and SQLite.

## Features

- Simple, clean user interface for posting messages
- Real-time message feed with auto-refresh capability
- Powerful keyword search using SQLite's FTS5 engine
- Zero-cost infrastructure (all components are free)
- Easy deployment to Streamlit Cloud or Heroku

## Tech Stack

- **Frontend/UI**: Streamlit
- **Backend**: Python
- **Database**: SQLite with FTS5 full-text search 
- **Search Engine**: SQLite FTS5

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/message-search-app.git
   cd message-search-app
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run app.py
   ```

## Usage

1. **Posting Messages**:
   - Navigate to the "Messages" tab
   - Enter your message in the text area
   - Click "Post Message"

2. **Viewing Messages**:
   - The message feed displays all messages in chronological order
   - Toggle auto-refresh to see new messages without manually reloading

3. **Searching Messages**:
   - Navigate to the "Search" tab
   - Enter keywords in the search box
   - View matching messages sorted by date

## Deployment

### Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Configure environment variables if needed

### Heroku
1. Create a Procfile with: `web: streamlit run app.py`
2. Create a runtime.txt with: `python-3.9.7`
3. Follow standard Heroku deployment procedures

## Data Persistence

The application uses SQLite for data storage, which creates a local file (`messages.db`). 
For cloud deployments, be aware that:

- On Streamlit Cloud: Data will persist as long as the app is deployed
- On Heroku: Data may be lost on dyno restarts unless you configure additional storage

## Future Enhancements

- User authentication system
- Message editing and deletion
- Advanced search filters
- Pagination for large message volumes
- API endpoints using FastAPI for programmatic access