# Flask-Graph-Content-Manager

A modular Flask application designed to manage AI agent sessions and dynamic content using the power of Neo4j graph databases. This project serves as a foundation for a modern, headless CMS with integrated AI interaction monitoring.

## 🚀 Overview

Flask-Graph-Content-Manager provides a centralized dashboard for tracking AI agent interactions and managing website content dynamically. By leveraging Neo4j, it maps complex relationships between domains, templates, and user sessions, offering a high-level view of how content is served and consumed.

## ✨ Key Features

### 🤖 AI Session Monitoring
*   **Session Listing**: View all active and historical sessions from AI agents.
*   **Interaction History**: Dive deep into individual sessions to view full chat history, including prompts, responses, and metadata.
*   **Real-time Tracking**: Monitor IP addresses and timestamps for the latest interactions.

### 📄 Graph-Based Content Management
*   **Domain-Specific Templates**: Content is organized by domain nodes, allowing for multi-tenant configurations.
*   **Dynamic Rendering**: Templates are fetched directly from Neo4j and rendered on-the-fly, enabling instant content updates without redeploying.
*   **SEO Management**: Integrated fields for Sitemap parameters (priority, change frequency, etc.) directly on content nodes.

### 🔒 Security & Scale
*   **Secure Authentication**: Protected routes using `Flask-Bcrypt` for password hashing and session-based access control.
*   **Blueprint Architecture**: Modular design for easy maintenance and feature expansion.

## 🛠️ Tech Stack

*   **Backend**: Python, [Flask](https://flask.palletsprojects.com/)
*   **Database**: [Neo4j](https://neo4j.com/) (Graph Database)
*   **Security**: Flask-Bcrypt
*   **Frontend**: Jinja2 Templates, Vanilla CSS

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/snowblow07/Flask-Graph-Content-Manager.git
    cd Flask-Graph-Content-Manager
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Update `database/db.py` with your Neo4j credentials:
    ```python
    NEO4J_URI = "neo4j+ssc://your-db-id.databases.neo4j.io"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "your-password"
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```
    The app will be available at `http://localhost:5050`.

## 🗺️ Roadmap (Next Steps)

*   [ ] **Full Headless CMS Integration**: Implementation of structured API endpoints for external content consumption.
*   [ ] **Rich Text Editor**: Integration of a GUI for template editing within the admin dashboard.
*   [ ] **Advanced Analytics**: Deeper insights into AI session patterns and content performance.

## 👤 Author

**Manuel Rosero Puente**
*   Email: [manuel.rosero@sheengreen.com](mailto:manuel.rosero@sheengreen.com)
*   GitHub: [ManuelRosero](https://github.com/snowblow07)

## 📄 License

This project is for portfolio purposes. Please contact the author for licensing inquiries.
