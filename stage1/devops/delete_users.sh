#!/bin/bash

# Logging file
LOG_FILE="/var/log/user_deletion.log"

# Ensure the log file exists and create it if it doesn't
touch $LOG_FILE

# Combined log and echo function
log_and_echo() {
    message="$(date +'%Y-%m-%d %H:%M:%S') - $1"
    echo $message
    echo $message >> $LOG_FILE
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

    log_and_echo "Processing user deletion: $username"

    # Check if user exists
    if id -u "$username" >/dev/null 2>&1; then
        # Delete the user and their home directory
        userdel -r "$username"
        if [ $? -eq 0 ]; then
            log_and_echo "User $username deleted along with home directory."
        else
            log_and_echo "Failed to delete user $username."
            continue
        fi

        # Check if the user's primary group exists and delete if only associated with the user
        if getent group "$username" >/dev/null 2>&1; then
            if ! getent passwd | grep -q ":$username:"; then
                groupdel "$username"
                if [ $? -eq 0 ]; then
                    log_and_echo "Primary group $username deleted."
                else
                    log_and_echo "Failed to delete primary group $username."
                fi
            fi
        fi
    else
        log_and_echo "User $username does not exist. Skipping deletion."
    fi

done < "$1"

log_and_echo "User deletion process completed."
