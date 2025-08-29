# How to Push Your ADK Agent Project to GitHub

This guide provides step-by-step instructions on how to initialize a Git repository for your ADK agent project (`gmail_manager` in this case) and push it to your GitHub account.

**Assumptions:**
*   You have Git installed on your system.
*   You have a GitHub account and have created a new, empty repository for this project (e.g., `gmail_manager` on your `Tradie-AI-2000` GitHub account).
*   Your project is located at `/Users/joeward/TradieAI Agents/Email Manager/gmail_manager`.

---

## Step 1: Navigate to Your Project Directory

Open your terminal and navigate to the root directory of your `gmail_manager` project:

```bash
cd "/Users/joeward/TradieAI Agents/Email Manager/gmail_manager"
```

## Step 2: Initialize a Git Repository

Initialize a new Git repository in your project directory:

```bash
git init
```

## Step 3: Create a `.gitignore` File

It's crucial to ignore files that should not be committed to Git, such as virtual environment files (`.venv/`) and sensitive environment variables (`.env`). Create a file named `.gitignore` in the root of your `gmail_manager` project (`/Users/joeward/TradieAI Agents/Email Manager/gmail_manager/.gitignore`) with the following content:

```
# Python virtual environment
.venv/

# Environment variables
.env
```

You can create this file using your text editor or by running:

```bash
echo -e "# Python virtual environment\n.venv/\n\n# Environment variables\n.env" > .gitignore
```

## Step 4: Add Your Files to the Staging Area

Add all your project files to the Git staging area. This prepares them for the first commit:

```bash
git add .
```

## Step 5: Make Your First Commit

Commit the staged files to your local repository. This creates a snapshot of your project:

```bash
git commit -m "Initial commit: Gmail Manager ADK Agent project setup"
```

## Step 6: Add Your GitHub Remote Repository

Connect your local Git repository to your empty GitHub repository. Replace `YOUR_GITHUB_USERNAME` with `Tradie-AI-2000` and `YOUR_REPOSITORY_NAME` with the name of the repository you created on GitHub (e.g., `gmail_manager`).

```bash
git remote add origin https://github.com/Tradie-AI-2000/gmail_manager.git
```
*(Note: You must create an empty repository named `gmail_manager` on your GitHub account `Tradie-AI-2000` before running this command.)*

## Step 7: Push Your Project to GitHub

Finally, push your local commits to your GitHub repository. The `-u` flag sets the upstream branch, so future `git push` commands will be simpler.

```bash
git push -u origin main
```
*(Note: GitHub's default branch name is often `main`. If your repository uses `master`, use `git push -u origin master` instead.)*

---

Your `gmail_manager` ADK agent project should now be live on your GitHub repository!

---

# How to Update an Existing Agent in GitHub

Once your agent project is on GitHub, updating it involves a standard Git workflow:

1.  **Make Local Changes:** Modify your agent's code, prompts, or configuration files as needed on your local machine.

2.  **Navigate to Project Directory:** Open your terminal and ensure you are in the root directory of your agent project (e.g., `cd "/Users/joeward/TradieAI Agents/Email Manager/gmail_manager"`).

3.  **Stage Your Changes:** Tell Git which changes you want to include in your next commit.
    ```bash
    git add .
    ```
    *(This stages all changes in the current directory and its subdirectories. You can also stage specific files, e.g., `git add gmail_manager/prompt.py`)*

4.  **Commit Your Changes:** Record the staged changes to your local repository with a descriptive message.
    ```bash
    git commit -m "Refined EmailDrafter tone and added examples"
    ```
    *(Example: `git commit -m "Refined EmailDrafter tone and added examples"`)*

5.  **Push to GitHub:** Send your committed changes from your local repository to your GitHub repository.
    ```bash
    git push
    ```
    *(If you followed the initial setup, `git push` alone should work. Otherwise, you might need `git push origin main` or `git push origin origin main` or `git push origin master` depending on your branch name.)*

Your updates will now be reflected on your GitHub repository!

---

# How to Delete a GitHub Repository

Deleting a GitHub repository is a permanent and irreversible action. It's typically done through the GitHub website for security and to prevent accidental data loss.

1.  **Go to GitHub:** Open your web browser and navigate to [github.com](https://github.com/).
2.  **Log In:** Log in to your GitHub account.
3.  **Navigate to the Repository:**
    *   On your GitHub homepage, find the repository you wish to delete in your list of repositories on the left sidebar, or use the search bar.
    *   Click on the repository's name to go to its main page.
4.  **Go to Settings:**
    *   On the repository's page, click on the **"Settings"** tab (usually located near the top, to the right of "Code," "Issues," "Pull requests," etc.).
5.  **Scroll to "Danger Zone":**
    *   On the Settings page, scroll all the way down until you find a section titled **"Danger Zone."**
6.  **Delete Repository:**
    *   Within the "Danger Zone," locate the **"Delete this repository"** option.
    *   Click the **"Delete this repository"** button.
7.  **Confirm Deletion:**
    *   A confirmation dialog will appear. You will be asked to type the exact name of the repository to confirm you understand the action is permanent.
    *   Type the repository name precisely as requested and click **"I understand the consequences, delete this repository."**

The repository will then be permanently deleted from your GitHub account.