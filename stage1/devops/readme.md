# User Creation Script

## Overview

This repository contains a bash script (`create_users.sh`) designed to automate the creation of users and groups on a Linux system. The script reads a text file containing usernames and their associated groups, creates the necessary users and groups, sets up home directories with appropriate permissions, generates random passwords for the users, and logs all actions.

## Features

- Create users and groups as specified in the input file.
- Assign multiple groups to users.
- Set up home directories with correct permissions.
- Generate random passwords for users.
- Log all actions to `/var/log/user_management.log`.
- Store generated passwords securely in `/var/secure/user_passwords.csv`.

## Requirements

- The script must be run with superuser (root) privileges.
- The input file must contain usernames and groups in the specified format.

## Input File Format

The input file should have one user per line, with the format:

```bash
    username;group1,group2,group3

```

## Usage

- **Clone the repository:**

```bash
    git clone https://github.com/incredible-phoenix246/hng11
    cd hng11/stage1/devops
```

- **Create the input file:**

-Create a text file named `users.txt` in the repository directory.
-Add the usernames and groups in the specified format.

**Make the script executable:**

```bash
    chmod +x create_users.sh
```

**Run the script:**

```bash
    sudo ./create_users.sh users.txt
```

**Logging and Password Storage**

- Log File: Actions performed by the script are logged to /var/log/user_management.log.
- Password File: Generated passwords are stored in /var/secure/user_passwords.csv with secure permissions.

**Verifying the Results**

- Check the log file:

  ```bash
      cat /var/log/user_management.log
  ```

- Check the password file:

  ```bash
      sudo cat /var/secure/user_passwords.csv
  ```

- Verify users and groups:

  ```bash
    getent passwd light
    getent group light
    getent group sudo
  ```

**Conclusion**
Automating user management in a Linux environment can significantly improve efficiency and reduce errors. By leveraging a bash script like create_users.sh, you can quickly and securely create users, assign groups, and set up home directories. This script ensures that all actions are logged and passwords are stored securely, making it a valuable tool for any SysOps engineer.
