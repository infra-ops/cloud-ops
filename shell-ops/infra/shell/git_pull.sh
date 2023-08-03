#!/bin/bash
# Set variables for the repository and the pull request
REPO_OWNER="nik786"
REPO_NAME="git-test-2"
PR_BODY="please review"
RELEASE_BRANCH="release/1.0" #"or any other base branch you want to merge into"
FEATURE_BRANCH="feature/1.0" #"your-branch-to-merge"
GIT_REPO="git@github.com:nik786/git-test-2.git"


COMMIT_MESSAGE="Jira-90876"

# Set variables for authentication
GITHUB_API_TOKEN="ghg"
AUTH_HEADER="Authorization: token $GITHUB_API_TOKEN"

# Construct the URL for the pull request API endpoint
API_URL="https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/pulls"

# Construct the JSON payload for the pull request
JSON_BODY=$(cat <<EOF
{
  "title": "$COMMIT_MESSAGE",
  "body": "$PR_BODY",
  "head": "$FEATURE_BRANCH",
  "base": "$RELEASE_BRANCH"
}
EOF
)


    git clone $GIT_REPO -b $FEATURE_BRANCH
    
    RN=$(basename "$GIT_REPO" .git)
    cd "$RN"
    #echo "$GIT_REPO" 
    # Copy the file to the repository directory

    # Add, commit, and push the file to the repository
    #git checkout $FEATURE_BRANCH
    printf "hello world" > 1.txt
    git add .
    git commit -m "$COMMIT_MESSAGE"
    git push 

    RESPONSE=$(curl -sk -X POST -H "$AUTH_HEADER" -d "$JSON_BODY" "$API_URL")
    echo $RESPONSE


    echo "Pull request created"
   
