#!/bin/bash

# Specify the numpy versions to try
numpy_versions=(
    "1.25.5"
    "1.25.4"
    "1.25.3"
    "1.25.2"
    "1.25.1"
    "1.25.0"
    "1.24.3"
    "1.24.2"
    "1.24.1"
    "1.24.0"
    "1.23.3"
    "1.23.2"
    "1.23.1"
    "1.23.0"
    "1.22.3"
    "1.22.2"
    "1.22.1"
    "1.22.0"
    "1.21.2"
    "1.21.1"
    "1.21.0"
    "1.20.3"
    "1.20.2"
    "1.20.1"
    "1.20.0"
    "1.19.5"
    "1.19.4"
    "1.19.3"
    "1.19.2"
    "1.19.1"
    "1.19.0"
    "1.18.5"
    "1.18.4"
    "1.18.3"
    "1.18.2"
    "1.18.1"
    "1.18.0"
    "1.17.5"
    "1.17.4"
    "1.17.3"
    "1.17.2"
    "1.17.1"
    "1.17.0"
    "1.16.6"
    "1.16.5"
    "1.16.4"
    "1.16.3"
    "1.16.2"
    "1.16.1"
    "1.16.0"
    # Add more versions as needed
)

# Loop through each numpy version
for version in "${numpy_versions[@]}"; do
    echo "Trying numpy version: $version"
    
    # Update the requirements.txt file with the current numpy version
    sed -i '' "s/^numpy.*/numpy==$version/" requirements.txt
    
    # Commit the changes
    git add requirements.txt
    git commit -m "Update numpy version to $version"
    
    # Push the changes to Heroku
    git push heroku main
    
    # Check if the push was successful
    if [ $? -eq 0 ]; then
        echo "Push to Heroku successful with numpy version: $version"
        exit 0
    else
        echo "Push to Heroku failed with numpy version: $version"
    fi
done

echo "None of the numpy versions were successfully pushed to Heroku."
exit 1
