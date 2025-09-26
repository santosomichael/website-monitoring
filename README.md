Of course. Here is a complete `README.md` file generated from our entire conversation. It explains the project, its structure, and how to set it up from scratch.

-----

# Automated Website Login Monitor

This project provides a fully automated system for monitoring a website's login functionality. It uses Playwright to simulate a user login, Docker to create a consistent testing environment, and Jenkins to schedule and orchestrate the entire process to run hourly.

## ✨ Features

  * **Automated Login Tests:** Uses Playwright to navigate to a login page, enter credentials, and verify a successful login.
  * **Scheduled Execution:** Jenkins CI/CD pipeline is configured to run the test automatically every hour.
  * **Consistent Environment:** Docker ensures that the tests run in a clean, isolated environment with all dependencies pre-installed, eliminating "it works on my machine" issues.
  * **Artifact Archiving:** Automatically saves screenshots of the test results (success or failure) as artifacts in Jenkins for easy review.

-----

## 📂 Project Structure

```
.
├── Dockerfile              # Blueprint for the Playwright test environment.
├── Jenkinsfile             # The CI/CD pipeline script for Jenkins.
├── app.py                  # The main Python script that runs the Playwright tests.
├── config.py               # Configuration file for the application.
├── docker-compose.yml      # Easy setup file to start the Jenkins server.
├── requirements.txt        # Python dependencies for the project.
├── screenshots/            # Directory where test screenshots are saved. (Will be created)
├── tests/
│   └── login.py          # Module containing the test logic.
├── .env                    # Local environment variables (DO NOT COMMIT).
└── .env.example            # Template for the environment variables.
```

-----

## 🔧 Prerequisites

Before you begin, ensure you have the following installed on your machine:

  * [Docker](https://www.docker.com/products/docker-desktop/)
  * [Git](https://git-scm.com/)

-----

## 🚀 Quick Start & Setup

Follow these steps to get the entire monitoring system up and running.

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd <your-repository-name>
```

### Step 2: Configure Environment Variables

The application uses an `.env` file for credentials.

1.  Create a copy of the example file:
    ```bash
    cp .env.example .env
    ```
2.  Edit the `.env` file and add your website's URL and login credentials:
    ```
    BASE_URL="https_your_website_com"
    USERNAME="your_username"
    PASSWORD="your_password"
    ```
    **Important:** The `.env` file is listed in `.gitignore` and should **never** be committed to your repository.

### Step 3: Start the Jenkins Server

The `docker-compose.yml` file makes starting Jenkins simple.

1.  Run the following command in your project's root directory:

    ```bash
    docker-compose up -d
    ```

2.  **Complete the Jenkins Setup Wizard:**

      * Navigate to `http://localhost:8080` in your browser.
      * Get the initial admin password by running: `docker logs jenkins-server`
      * Follow the on-screen instructions, selecting **"Install suggested plugins"**.
      * Create your admin user.

3.  **Grant Jenkins Docker Permissions:** This is a crucial one-time setup step.

      * Find your host's Docker group ID: `grep 'docker' /etc/group | cut -d: -f3`
      * Use the ID to grant permissions to the Jenkins container:
        ```bash
        # Replace 'YOUR_DOCKER_GROUP_ID' with the number from the command above
        docker exec -u root jenkins-server groupadd -g YOUR_DOCKER_GROUP_ID docker
        docker exec -u root jenkins-server usermod -aG docker jenkins
        ```
      * Restart Jenkins for the changes to take effect:
        ```bash
        docker restart jenkins-server
        ```

### Step 4: Configure the Jenkins Job

1.  On your Jenkins dashboard, click **"New Item"**.
2.  Enter a name (e.g., "Website-Monitor-Pipeline") and select **"Pipeline"**.
3.  Scroll down to the **"Pipeline"** section and select **"Pipeline script from SCM"**.
4.  Choose **"Git"** and enter your repository's URL.
5.  Ensure the **"Script Path"** is `Jenkinsfile`.
6.  Click **"Save"**.

Your pipeline is now configured\! It will run automatically every hour. You can also trigger it manually by clicking **"Build Now"**.

-----

## ⚙️ How It Works

The automation flow is managed by the `Jenkinsfile`:

1.  **Trigger:** The pipeline is triggered automatically every hour by a `cron` schedule.
2.  **Checkout:** Jenkins checks out the latest code from your Git repository into a clean workspace.
3.  **Build:** Jenkins uses the `Dockerfile` to build a fresh, clean Docker image containing Playwright and your Python scripts.
4.  **Run:** Jenkins runs a container from the newly built image. The `app.py` script executes, performing the login test.
5.  **Archive:** After the run, Jenkins collects any `.png` files from the `screenshots` directory and saves them as **build artifacts**, which you can view from the build's page.
6.  **Cleanup:** The workspace and Docker image are cleaned up to save space.

-----

## quản lý Managing the Service

  * **To stop the Jenkins server:**
    ```bash
    docker-compose down
    ```
  * **To view the logs of the Jenkins server:**
    ```bash
    docker logs -f jenkins-server
    ```