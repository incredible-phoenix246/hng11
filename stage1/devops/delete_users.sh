#!/bin/bash

# Logging file
LOG_FILE="/var/log/user_deletion.log"

# Ensure the log file exists and create it if it doesn't
touch $LOG_FILE

# Log message function
log_message() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" >> $LOG_FILE
}

# Check if a file was provided
if [ -z "$1" ]; then
    echo "Usage: bash delete_users.sh <name-of-text-file>"
    exit 1
fi

# Read the file line by line
while IFS=';' read -r username groups; do
    # Remove leading/trailing whitespaces
    username=$(echo $username | xargs)

    # Skip empty lines
    if [ -z "$username" ]; then
        continue
    fi

    echo "Processing user deletion: $username"

    # Check if user exists
    if id -u "$username" >/dev/null 2>&1; then
        # Delete the user and their home directory
        userdel -r "$username"
        if [ $? -eq 0 ]; then
            log_message "User $username deleted along with home directory."
            echo "User $username deleted along with home directory."
        else
            log_message "Failed to delete user $username."
            echo "Failed to delete user $username."
            continue
        fi

        # Check if the user's primary group exists and delete if only associated with the user
        if getent group "$username" >/dev/null 2>&1; then
            if ! getent passwd | grep -q ":$username:"; then
                groupdel "$username"
                if [ $? -eq 0 ]; then
                    log_message "Primary group $username deleted."
                    echo "Primary group $username deleted."
                else
                    log_message "Failed to delete primary group $username."
                    echo "Failed to delete primary group $username."
                fi
            fi
        fi
    else
        log_message "User $username does not exist. Skipping deletion."
        echo "User $username does not exist. Skipping deletion."
    fi

done < "$1"

log_message "User deletion process completed."
echo "User deletion process completed."
