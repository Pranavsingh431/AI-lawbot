#!/bin/bash

# Colors for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=============================================${NC}"
echo -e "${GREEN}Legal Advisor AI - Deployment Script${NC}"
echo -e "${BLUE}=============================================${NC}"

# Check requirements
check_requirements() {
    echo -e "\n${BLUE}Checking requirements...${NC}"
    
    # Check if Python is installed
    if ! command -v python &> /dev/null; then
        echo -e "${RED}Python is not installed. Please install Python 3.8 or higher.${NC}"
        exit 1
    fi
    
    # Check Python version
    python_version=$(python --version 2>&1 | awk '{print $2}')
    python_major=$(echo $python_version | cut -d. -f1)
    python_minor=$(echo $python_version | cut -d. -f2)
    
    if [ "$python_major" -lt 3 ] || ([ "$python_major" -eq 3 ] && [ "$python_minor" -lt 8 ]); then
        echo -e "${RED}Python version 3.8 or higher is required. Found: $python_version${NC}"
        exit 1
    fi
    
    # Check if pip is installed
    if ! command -v pip &> /dev/null; then
        echo -e "${RED}pip is not installed. Please install pip.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}All requirements satisfied.${NC}"
}

# Install dependencies
install_dependencies() {
    echo -e "\n${BLUE}Installing dependencies...${NC}"
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to install dependencies.${NC}"
            exit 1
        fi
    else
        echo -e "${RED}requirements.txt not found.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Dependencies installed successfully.${NC}"
}

# Setup streamlit config
setup_streamlit_config() {
    echo -e "\n${BLUE}Setting up Streamlit configuration...${NC}"
    
    mkdir -p ~/.streamlit
    
    cat > ~/.streamlit/config.toml << EOF
[server]
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
EOF
    
    echo -e "${GREEN}Streamlit configuration created.${NC}"
}

# Deploy to Streamlit Cloud
deploy_to_streamlit_cloud() {
    echo -e "\n${BLUE}Preparing for Streamlit Cloud deployment...${NC}"
    
    if ! command -v git &> /dev/null; then
        echo -e "${RED}Git is required for Streamlit Cloud deployment.${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Please follow these steps to deploy to Streamlit Cloud:${NC}"
    echo -e "1. Make sure your code is in a GitHub repository."
    echo -e "2. Visit https://streamlit.io/cloud and sign in."
    echo -e "3. Click 'New app' and connect to your GitHub repository."
    echo -e "4. Set the main file path to 'app.py'."
    echo -e "5. Add your secrets from .env file in the 'Advanced settings' section."
    
    read -p "Do you want to upload to GitHub now? (y/n): " github_choice
    if [[ $github_choice == "y" || $github_choice == "Y" ]]; then
        bash github_upload.sh
    fi
    
    echo -e "${GREEN}Follow the instructions above to complete the Streamlit Cloud deployment.${NC}"
}

# Deploy to Heroku
deploy_to_heroku() {
    echo -e "\n${BLUE}Preparing for Heroku deployment...${NC}"
    
    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        echo -e "${RED}Heroku CLI is not installed.${NC}"
        echo -e "${YELLOW}Please install the Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli${NC}"
        exit 1
    fi
    
    # Check if git is installed
    if ! command -v git &> /dev/null; then
        echo -e "${RED}Git is required for Heroku deployment.${NC}"
        exit 1
    fi
    
    # Check if user is logged in to Heroku
    heroku whoami &> /dev/null
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}Please log in to Heroku:${NC}"
        heroku login
    fi
    
    # Create a new Heroku app
    read -p "Enter a name for your Heroku app (leave blank for random name): " heroku_app_name
    
    if [ -z "$heroku_app_name" ]; then
        heroku create
    else
        heroku create "$heroku_app_name"
    fi
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create Heroku app.${NC}"
        exit 1
    fi
    
    # Set environment variables from .env
    if [ -f ".env" ]; then
        echo -e "${YELLOW}Setting environment variables from .env file...${NC}"
        while IFS= read -r line || [[ -n "$line" ]]; do
            # Skip comments and empty lines
            [[ "$line" =~ ^#.*$ ]] && continue
            [[ -z "$line" ]] && continue
            
            # Extract variable name and value
            var_name=$(echo "$line" | cut -d '=' -f 1)
            var_value=$(echo "$line" | cut -d '=' -f 2-)
            
            # Set environment variable on Heroku
            heroku config:set "$var_name=$var_value"
        done < ".env"
    else
        echo -e "${YELLOW}No .env file found. Please manually set environment variables.${NC}"
    fi
    
    # Deploy to Heroku
    echo -e "${YELLOW}Deploying to Heroku...${NC}"
    git push heroku master || git push heroku main
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to deploy to Heroku.${NC}"
        exit 1
    fi
    
    # Scale the dyno
    heroku ps:scale web=1
    
    echo -e "${GREEN}Deployed to Heroku successfully.${NC}"
    heroku open
}

# Deploy with Docker
deploy_with_docker() {
    echo -e "\n${BLUE}Preparing for Docker deployment...${NC}"
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Docker is not installed.${NC}"
        echo -e "${YELLOW}Please install Docker from: https://docs.docker.com/get-docker/${NC}"
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${YELLOW}Docker Compose is not installed. Only basic Docker deployment will be available.${NC}"
        docker_compose_available=false
    else
        docker_compose_available=true
    fi
    
    # Docker deployment options
    echo -e "${YELLOW}Choose Docker deployment method:${NC}"
    echo -e "1. Deploy with Docker Compose (recommended)"
    echo -e "2. Deploy with Docker only"
    
    if [ "$docker_compose_available" = false ]; then
        echo -e "${RED}Option 1 is not available because Docker Compose is not installed.${NC}"
        deploy_option=2
    else
        read -p "Enter your choice (1/2): " deploy_option
    fi
    
    case $deploy_option in
        1)
            # Deploy with Docker Compose
            echo -e "${YELLOW}Deploying with Docker Compose...${NC}"
            
            # Check if docker-compose.yml exists
            if [ ! -f "docker-compose.yml" ]; then
                echo -e "${RED}docker-compose.yml not found.${NC}"
                exit 1
            fi
            
            # Deploy
            docker-compose up -d
            
            if [ $? -ne 0 ]; then
                echo -e "${RED}Failed to deploy with Docker Compose.${NC}"
                exit 1
            fi
            
            echo -e "${GREEN}Deployed with Docker Compose successfully.${NC}"
            echo -e "${YELLOW}Your application is running at: http://localhost:8501${NC}"
            ;;
        2)
            # Deploy with Docker only
            echo -e "${YELLOW}Deploying with Docker...${NC}"
            
            # Check if Dockerfile exists
            if [ ! -f "Dockerfile" ]; then
                echo -e "${RED}Dockerfile not found.${NC}"
                exit 1
            fi
            
            # Build Docker image
            docker build -t legal-advisor-ai .
            
            if [ $? -ne 0 ]; then
                echo -e "${RED}Failed to build Docker image.${NC}"
                exit 1
            fi
            
            # Run Docker container
            docker run -d -p 8501:8501 --name legal-advisor-ai --env-file .env legal-advisor-ai
            
            if [ $? -ne 0 ]; then
                echo -e "${RED}Failed to run Docker container.${NC}"
                exit 1
            fi
            
            echo -e "${GREEN}Deployed with Docker successfully.${NC}"
            echo -e "${YELLOW}Your application is running at: http://localhost:8501${NC}"
            ;;
        *)
            echo -e "${RED}Invalid option.${NC}"
            exit 1
            ;;
    esac
}

# Deploy to AWS
deploy_to_aws() {
    echo -e "\n${BLUE}Preparing for AWS deployment...${NC}"
    
    # Check if AWS CLI is installed
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}AWS CLI is not installed.${NC}"
        echo -e "${YELLOW}Please install AWS CLI from: https://aws.amazon.com/cli/${NC}"
        exit 1
    fi
    
    # Check if Elastic Beanstalk CLI is installed
    if ! command -v eb &> /dev/null; then
        echo -e "${RED}Elastic Beanstalk CLI is not installed.${NC}"
        echo -e "${YELLOW}Please install EB CLI: pip install awsebcli${NC}"
        exit 1
    fi
    
    # Check AWS configuration
    aws sts get-caller-identity &> /dev/null
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}Please configure AWS credentials:${NC}"
        aws configure
    fi
    
    # Create Elastic Beanstalk application
    echo -e "${YELLOW}Initializing Elastic Beanstalk application...${NC}"
    eb init -p python-3.8 legal-advisor-ai
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to initialize Elastic Beanstalk application.${NC}"
        exit 1
    fi
    
    # Create Elastic Beanstalk environment
    echo -e "${YELLOW}Creating Elastic Beanstalk environment...${NC}"
    eb create legal-advisor-ai-env
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create Elastic Beanstalk environment.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Deployed to AWS Elastic Beanstalk successfully.${NC}"
    eb open
}

# Run locally
run_locally() {
    echo -e "\n${BLUE}Running application locally...${NC}"
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}No .env file found. Creating from .env.example...${NC}"
        
        if [ -f ".env.example" ]; then
            cp .env.example .env
            echo -e "${YELLOW}Please edit .env file to add your API keys.${NC}"
        else
            echo -e "${RED}.env.example not found.${NC}"
            exit 1
        fi
    fi
    
    # Run the application
    streamlit run app.py
}

# Main menu
main_menu() {
    echo -e "\n${BLUE}Choose deployment option:${NC}"
    echo -e "1. Run locally"
    echo -e "2. Deploy to Streamlit Cloud"
    echo -e "3. Deploy with Docker"
    echo -e "4. Deploy to Heroku"
    echo -e "5. Deploy to AWS Elastic Beanstalk"
    echo -e "6. Exit"
    
    read -p "Enter your choice (1-6): " choice
    
    case $choice in
        1)
            check_requirements
            install_dependencies
            setup_streamlit_config
            run_locally
            ;;
        2)
            check_requirements
            install_dependencies
            deploy_to_streamlit_cloud
            ;;
        3)
            deploy_with_docker
            ;;
        4)
            check_requirements
            install_dependencies
            deploy_to_heroku
            ;;
        5)
            check_requirements
            install_dependencies
            deploy_to_aws
            ;;
        6)
            echo -e "${GREEN}Exiting.${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please try again.${NC}"
            main_menu
            ;;
    esac
}

# Start the script
main_menu 