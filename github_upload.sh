#!/bin/bash

# Colors for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=============================================${NC}"
echo -e "${GREEN}Legal Advisor AI - GitHub Upload Script${NC}"
echo -e "${BLUE}=============================================${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Git is not installed. Please install git first.${NC}"
    exit 1
fi

# Check if the project is already a git repository
if [ -d .git ]; then
    echo -e "${YELLOW}This project is already a git repository.${NC}"
    read -p "Do you want to continue with the existing repository? (y/n): " continue_existing
    if [[ $continue_existing != "y" && $continue_existing != "Y" ]]; then
        echo -e "${RED}Aborting.${NC}"
        exit 1
    fi
else
    # Initialize git repository
    echo -e "${GREEN}Initializing git repository...${NC}"
    git init
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to initialize git repository.${NC}"
        exit 1
    fi
fi

# Create GitHub repository
echo -e "\n${BLUE}Creating GitHub Repository${NC}"
echo -e "${YELLOW}You can create a new GitHub repository in two ways:${NC}"
echo -e "1. Using GitHub CLI (if installed)"
echo -e "2. Manually through the GitHub website"
read -p "Choose an option (1/2): " github_option

if [ "$github_option" == "1" ]; then
    # Check if GitHub CLI is installed
    if ! command -v gh &> /dev/null; then
        echo -e "${RED}GitHub CLI is not installed. Please install it first or choose option 2.${NC}"
        echo -e "Visit: https://cli.github.com/manual/installation"
        github_option=2
    else
        echo -e "${GREEN}Creating repository using GitHub CLI...${NC}"
        read -p "Enter repository name (default: legal-advisor-ai): " repo_name
        repo_name=${repo_name:-legal-advisor-ai}
        read -p "Enter repository description: " repo_description
        read -p "Make repository private? (y/n): " private_choice
        
        private_flag=""
        if [[ $private_choice == "y" || $private_choice == "Y" ]]; then
            private_flag="--private"
        else
            private_flag="--public"
        fi
        
        gh auth login
        gh repo create "$repo_name" --description "$repo_description" $private_flag
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to create GitHub repository.${NC}"
            exit 1
        fi
        
        # Set remote origin
        git remote add origin "https://github.com/$(gh api user | jq -r .login)/$repo_name.git"
    fi
fi

if [ "$github_option" == "2" ]; then
    echo -e "\n${YELLOW}Please follow these steps:${NC}"
    echo -e "1. Go to https://github.com/new"
    echo -e "2. Enter a repository name (e.g., legal-advisor-ai)"
    echo -e "3. Add an optional description"
    echo -e "4. Choose public or private"
    echo -e "5. Do NOT initialize with README, .gitignore, or license"
    echo -e "6. Click 'Create repository'"
    echo -e "7. Copy the repository URL"
    
    read -p "Press Enter when you've created the repository and have the URL ready..."
    read -p "Enter the GitHub repository URL: " repo_url
    
    # Set remote origin
    git remote add origin "$repo_url"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to add remote origin.${NC}"
        exit 1
    fi
fi

# Stage files
echo -e "\n${GREEN}Staging files...${NC}"
git add .
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to stage files.${NC}"
    exit 1
fi

# Commit changes
echo -e "\n${GREEN}Committing files...${NC}"
read -p "Enter commit message (default: Initial commit): " commit_message
commit_message=${commit_message:-"Initial commit"}

git commit -m "$commit_message"
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to commit files.${NC}"
    exit 1
fi

# Push to GitHub
echo -e "\n${GREEN}Pushing to GitHub...${NC}"
echo -e "${YELLOW}This may prompt for your GitHub username and password or token.${NC}"
git push -u origin main || git push -u origin master

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Push failed. Trying to set up the main branch...${NC}"
    git branch -M main
    git push -u origin main
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to push to GitHub. Please check your credentials and try again.${NC}"
        echo -e "${YELLOW}If you're using password authentication, note that GitHub no longer supports it.${NC}"
        echo -e "${YELLOW}Please use a personal access token instead: https://github.com/settings/tokens${NC}"
        exit 1
    fi
fi

echo -e "\n${GREEN}Success! Your project has been uploaded to GitHub.${NC}"
echo -e "${BLUE}=============================================${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo -e "1. Visit your GitHub repository to verify the upload"
echo -e "2. Set up GitHub Pages if you want to showcase your project"
echo -e "3. Consider adding collaborators to your project"
echo -e "${BLUE}=============================================${NC}" 