# Project Setup and Documentation

This document outlines the steps to configure and run the application, including setting up database credentials, Redis configuration, and handling video operations. It also provides a detailed overview of the core features and functionality of the project.

## Project Overview

This application is designed to support both user and admin workflows, focusing on video management functionality. Below are the key features:

### Features

- **User and Admin Registration/Login**  
  Users and administrators must register and authenticate to access the platform.

- **Video Management Operations**  
  - **Video Upload**: Admins can upload videos to the system via a dedicated API endpoint.
  - **Video Download**: Users and admins can download videos from the system.
  - **Video Search**: Admins can search by video file name or video size.
  - **Block Videos**: Admins and users can block specific videos by their unique video ID.
  - **Unblock Videos**: Admins and users can unblock specific videos by their unique video ID.

> **Note**: Video upload functionality and search functionality are restricted to admins. Ensure registration and login are completed before accessing any video-related operations.

## Prerequisites

To run the application, ensure the following tools and services are installed and available:

- **Docker**: To containerize and deploy the application.
- **Docker Compose**: To manage multi-container Docker applications.
- **Local Network Access**: For proper communication between services.

## Configuration Instructions

### Configure `config.ini` for Docker

When running the application inside Docker containers, the configuration for the database and Redis services must be updated to use the local network IP address. This allows proper communication between Docker services and external resources.

**Steps**:

1. Locate the `config.ini` file in the root directory of the project.
2. Update the following sections with your specific environment details:

   ```ini
   [database]
   db_host = <LOCAL_NETWORK_IP> ; Replace with your machine's local network IP
   db_port = <DB_PORT>           ; Default port for the database (e.g., 3306 for MySQL)
   db_user = <DB_USERNAME>       ; Database username
   db_password = <DB_PASSWORD>   ; Database password
   db_name = <DB_NAME>           ; Database name

   [redis]
   redis_host = <LOCAL_NETWORK_IP> ; Replace with your machine's local network IP
   redis_port = <REDIS_PORT>        ; Default port for Redis (e.g., 6379)
