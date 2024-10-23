# Monitoring Stack Deployment with Ansible

Welcome to the Monitoring Stack Deployment project! This repository provides an automated solution to deploy a comprehensive monitoring stack using Ansible. The stack includes Prometheus, Grafana, Loki, AlertManager, Node Exporter, and cAdvisor, orchestrated with Docker containers. The setup is designed for testing purposes and suitable for development environments.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Introduction
Effective monitoring is crucial for maintaining the health and performance of your infrastructure. This project automates the deployment of a robust monitoring stack using Ansible, ensuring that you can quickly set up and manage your monitoring tools.

The stack includes:

- **Prometheus**: Collects metrics from configured targets at given intervals.
- **Grafana**: Visualizes data through rich dashboards.
- **Loki**: Provides log aggregation and querying.
- **AlertManager**: Handles alerts sent by client applications like Prometheus.
- **Node Exporter**: Exposes machine metrics.
- **cAdvisor**: Collects container metrics.

## Features
- **Automated Deployment**: Use Ansible playbooks to deploy the entire monitoring stack with a single command.
- **Dockerized Services**: All components run in Docker containers for isolation and ease of management.
- **Scalable Architecture**: Easily add more nodes or services to your monitoring setup.
- **Customizable Configuration**: Templates and variables allow you to tailor configurations to your needs.
- **Local Development with Vagrant**: Test the stack locally using Vagrant and VirtualBox.
- **Automated Testing**: Ensure reliability with pytest and testinfra tests.

## Prerequisites
Before you begin, ensure you have the following installed on your control machine (the machine from which you'll run the Ansible playbooks):

1. **Ansible**
   - **Installation**:
     ```bash
     # For Ubuntu/Debian
     sudo apt update
     sudo apt install ansible -y

     # For macOS using Homebrew
     brew install ansible
     ```
   - **Version Check**:
     ```bash
     ansible --version
     ```

2. **Python and pip**
   - **Installation**:
     ```bash
     # For Ubuntu/Debian
     sudo apt install python3 python3-pip -y

     # For macOS using Homebrew
     brew install python
     ```
   - **Version Check**:
     ```bash
     python3 --version
     pip3 --version
     ```

3. **Git**
   - **Installation**:
     ```bash
     # For Ubuntu/Debian
     sudo apt install git -y

     # For macOS using Homebrew
     brew install git
     ```
   - **Version Check**:
     ```bash
     git --version
     ```

4. **Vagrant** (Optional, for local development)
   - **Installation**: [Download from Vagrant Downloads](https://www.vagrantup.com/downloads) and follow the installation instructions for your operating system.
   - **Version Check**:
     ```bash
     vagrant --version
     ```

5. **Docker** (On Target Hosts)
   - Note: The Ansible playbooks include roles to install Docker on target hosts. However, if you prefer to install Docker manually:
     ```bash
     # For Ubuntu/Debian
     sudo apt update
     sudo apt install docker-ce docker-ce-cli containerd.io -y
     ```

## Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/Aazme/monitoring-stack-ansible.git
   cd monitoring-stack-ansible
   ```

2. **Configure Ansible Inventory**
   - **Inventory File**: Edit `inventory/inventory.yml` to include your target hosts.
   
     Example:
     ```yaml
     all:
       hosts:
         monitoring-server:
           ansible_host: your_server_ip
           ansible_user: your_ssh_user
           ansible_ssh_private_key_file: path_to_your_private_key
     ```
   - **Vagrant Inventory (Optional)**: For local development with Vagrant, use `inventory/vagrant_inventory.yml`.

3. **Update Variables (If Necessary)**
   - **Ansible Configuration**: Review and update `ansible.cfg` if needed.
   - **Role Variables**: Customize variables in `playbooks/roles/*/vars/main.yml` as required.

4. **Install Python Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```
   **Requirements File (`requirements.txt`)**:
   ```txt
   ansible
   pytest
   testinfra
   ```

5. **(Optional) Set Up Vagrant for Local Testing**
   - **Start the Vagrant VM**:
     ```bash
     vagrant up
     ```
   - **SSH into the VM**:
     ```bash
     vagrant ssh monitoring-server
     ```

6. **Run the Ansible Playbook**
   ```bash
   ansible-playbook playbooks/site.yml
   ```
   - `playbooks/site.yml` is the main playbook that includes all roles.

## Usage
### Accessing the Monitoring Stack
- **Prometheus**:
  - **URL**: `http://your_server_ip:9090`
- **Grafana**:
  - **URL**: `http://your_server_ip:3000`
  - **Default Credentials**:
    - Username: `admin`
    - Password: `admin` (change after first login)
- **AlertManager**:
  - **URL**: `http://your_server_ip:9093`
- **Loki**:
  - **URL**: `http://your_server_ip:3100`

### Exploring Metrics and Logs
- **Node Exporter Metrics**:
  - Metrics endpoint: `http://your_server_ip:9100/metrics`
- **cAdvisor Metrics**:
  - Metrics endpoint: `http://your_server_ip:8080/metrics`

### Customizing Dashboards
- **Grafana Dashboards**:
  - Import existing dashboards or create new ones.
  - Use the provided dashboard template (`grafana_dashboard.json.j2`) as a starting point.

### Configuring Telegram Alerts
To configure Telegram alerts in AlertManager, you need to update the `alertmanager/defaults/main.yml` file with your Telegram bot token and chat ID:

**File**: `alertmanager/defaults/main.yml`
```yaml
---
telegram_bot_token: "7747059131:AAFZGqnsFFC7u-XXXXXXXXXXXXXXXX"
telegram_chat_id: "-100XXXXXXXXX"
```
Replace the placeholders with your actual Telegram bot token and chat ID. This configuration will allow AlertManager to send alerts to your specified Telegram chat.

## Testing
### Running Automated Tests
1. **Install Test Dependencies**
   ```bash
   pip3 install pytest testinfra
   ```

2. **Run the Tests**
   ```bash
    pytest --ansible-inventory=./inventory/inventory.yml --force-ansible --connection=ansible
   ```

### Manual Testing
1. **SSH into Target Host**
   ```bash
   ssh your_ssh_user@your_server_ip
   ```
2. **Check Docker Containers**
   ```bash
   docker ps
   ```
3. **Verify Services**
   ```bash
   systemctl status docker
   ```

## Troubleshooting
### Common Issues and Solutions
1. **SSH Connection Errors**
   - **Symptom**: Ansible reports `UNREACHABLE` or SSH errors.
   - **Solution**: Verify SSH connectivity to the target host and ensure SSH user and key are correctly specified.

2. **Permission Denied Errors**
   - **Symptom**: Containers fail to access necessary resources.
   - **Solution**: Check file permissions on configuration directories and ensure appropriate permissions for Docker socket.

3. **Services Not Running**
   - **Symptom**: Docker containers or services are not running.
   - **Solution**: Use `docker logs container_name` to view logs and check for configuration errors.

### Gathering More Information
- **Ansible Verbose Mode**: Run playbooks with increased verbosity:
  ```bash
  ansible-playbook playbooks/site.yml -vvv
  ```
- **System Logs**: Check system logs on the target host for errors:
  ```bash
  journalctl -xe
  ```
- **Docker Logs**: View logs for individual containers:
  ```bash
  docker logs prometheus
  ```

## Contributing
We welcome contributions to enhance the functionality and usability of this project.

### How to Contribute
1. **Fork the Repository**
   - Create a personal fork of the repository on GitHub.

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/Aazme/monitoring-stack-ansible.git
   cd monitoring-stack-ansible
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**
   - Follow coding standards and best practices.
   - Update or add documentation as necessary.
   - Write or update tests to cover your changes.

5. **Commit Your Changes**
   - Use Conventional Commits for commit messages.
   ```bash
   git commit -m "feat: add new feature X"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Go to the repository on GitHub and open a pull request.
   - Provide a clear description of your changes.

### Code of Conduct
Please read and adhere to the Code of Conduct.

### Contributing Guidelines
Refer to the Contributing Guide for detailed instructions.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- **Ansible Community**: For providing extensive documentation and support.
- **Prometheus and Grafana Teams**: For creating powerful monitoring tools.
- **Open Source Contributors**: For their valuable contributions to the tools used in this project.

## Additional Resources
- [Ansible Documentation](https://docs.ansible.com/ansible/latest/index.html)
- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Loki Documentation](https://grafana.com/docs/loki/latest/)

## Contact Information
For questions or support, please open an issue on the GitHub repository or contact the maintainer:

- **GitHub**: [https://github.com/Aazme/monitoring-stack-ansible](https://github.com/Aazme/monitoring-stack-ansible)
- **Email**: your.email@example.com
