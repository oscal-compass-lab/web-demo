#!/usr/bin/env python3
# Copyright (c) 2026 The OSCAL Compass Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Common server configuration data for Ubuntu hosts
This file provides a centralized source of truth for all Ubuntu server configurations
used across the document creation process.
"""

# Ubuntu server configurations
UBUNTU_SERVERS = [
    {
        "name": "ubuntu-web-01",
        "hostname": "ubuntu-web-01.example.com",
        "ip": "192.168.1.101",
        "description": "Primary web server running Ubuntu 24.04 LTS",
        "compliance_rate": 0.85,  # 85% pass rate
        "role": "web",
        "environment": "production"
    },
    {
        "name": "ubuntu-web-02",
        "hostname": "ubuntu-web-02.example.com",
        "ip": "192.168.1.102",
        "description": "Secondary web server running Ubuntu 24.04 LTS",
        "compliance_rate": 0.80,  # 80% pass rate
        "role": "web",
        "environment": "production"
    },
    {
        "name": "ubuntu-web-03",
        "hostname": "ubuntu-web-03.example.com",
        "ip": "192.168.1.106",
        "description": "Tertiary web server running Ubuntu 24.04 LTS",
        "compliance_rate": 0.88,  # 88% pass rate
        "role": "web",
        "environment": "production"
    },
    {
        "name": "ubuntu-db-01",
        "hostname": "ubuntu-db-01.example.com",
        "ip": "192.168.1.103",
        "description": "Database server running Ubuntu 24.04 LTS",
        "compliance_rate": 0.90,  # 90% pass rate
        "role": "database",
        "environment": "production"
    },
    {
        "name": "ubuntu-app-01",
        "hostname": "ubuntu-app-01.example.com",
        "ip": "192.168.1.104",
        "description": "Application server running Ubuntu 24.04 LTS",
        "compliance_rate": 0.75,  # 75% pass rate
        "role": "application",
        "environment": "production"
    },
    {
        "name": "ubuntu-mgmt-01",
        "hostname": "ubuntu-mgmt-01.example.com",
        "ip": "192.168.1.105",
        "description": "Management and monitoring server running Ubuntu 24.04 LTS",
        "compliance_rate": 0.95,  # 95% pass rate
        "role": "management",
        "environment": "production"
    }
]


def get_all_servers():
    """
    Get all Ubuntu server configurations.
    
    Returns:
        list: List of server configuration dictionaries
    """
    return UBUNTU_SERVERS


def get_server_by_name(name):
    """
    Get a specific server configuration by name.
    
    Args:
        name (str): Server name (e.g., 'ubuntu-web-01')
    
    Returns:
        dict: Server configuration dictionary or None if not found
    """
    for server in UBUNTU_SERVERS:
        if server['name'] == name:
            return server
    return None


def get_servers_by_role(role):
    """
    Get all servers with a specific role.
    
    Args:
        role (str): Server role (e.g., 'web', 'database', 'application', 'management')
    
    Returns:
        list: List of server configuration dictionaries matching the role
    """
    return [server for server in UBUNTU_SERVERS if server['role'] == role]


def get_servers_by_environment(environment):
    """
    Get all servers in a specific environment.
    
    Args:
        environment (str): Environment name (e.g., 'production', 'staging', 'development')
    
    Returns:
        list: List of server configuration dictionaries matching the environment
    """
    return [server for server in UBUNTU_SERVERS if server['environment'] == environment]


# Made with Bob