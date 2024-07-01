#!/bin/bash

# Logging and password storage files
LOG_FILE="/var/log/user_management.log"
PASSWORD_FILE="/var/secure/user_passwords.csv"

# Ensure the secure directory exists
mkdir -p /var/secure

# Ensure the log file exists and create it if it doesn't
touch $LOG_FILE

# Ensure the password file exists and set the correct permissions
touch $PASSWORD_FILE
chmod 600 $PASSWORD_FILE

# Combined log and echo function
log_and_echo() {
    message="$(date +'%Y-%m-%d %H:%M:%S') - $1"
    echo $message
    echo $message >> $LOG_FILE
}

# Function to generate random passwords
generate_password() {
    tr -dc 'A-Za-z0-9' </dev/urandom | head -c 12
}

# Check if a file was provided
if [ -z "$1" ]; then
    echo "Usage: bash create_users.sh <name-of-text-file>"
    exit 1
fi

# Read the file line by line
while IFS=';' read -r username groups; do
    # Remove leading/trailing whitespaces
    username=$(echo $username | xargs)
    groups=$(echo $groups | xargs)

    # Skip empty lines
    if [ -z "$username" ]; then
        continue
    fi

    log_and_echo "Processing user: $username"

    # Check if user already exists
    if id -u "$username" >/dev/null 2>&1; then
        log_and_echo "User $username already exists. Skipping creation."
        continue
    fi

    # Create a user-specific group if it doesn't exist
    if ! getent group "$username" >/dev/null 2>&1; then
        groupadd "$username"
        log_and_echo "Group $username created."
    fi

    # Create the user with the specific group
    useradd -m -g "$username" "$username" && log_and_echo "User $username created with primary group $username."

    # Assign additional groups
    IFS=',' read -ra additional_groups <<< "$groups"
    for group in "${additional_groups[@]}"; do
        group=$(echo $group | xargs)  # Remove leading/trailing whitespaces
        if [ -n "$group" ] && ! getent group "$group" >/dev/null 2>&1; then
            groupadd "$group"
            log_and_echo "Group $group created."
        fi
        usermod -aG "$group" "$username" && log_and_echo "User $username added to group $group."
    done

    # Generate a random password
    password=$(generate_password)

    # Set the user's password
    echo "$username:$password" | chpasswd && log_and_echo "Password set for user $username."

    # Store the username and password securely
    echo "$username,$password" >> $PASSWORD_FILE

    # Set home directory permissions
    chmod 700 "/home/$username" && log_and_echo "Permissions set for user $username's home directory."

done < "$1"

log_and_echo "User creation process completed."
echo "User creation process completed."
