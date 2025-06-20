# Installation
As this repository is not yet added in HACS you have to install it manually.

1. Download or clone the repository
2. Copy the files from custom_components/beszel-api into your HomeAssistant's config/custom_components/ directory under a new directory called "beszel-api"
3. Restart HomeAssistant
4. Go to integrations, press Add integration and search for BeszelAPI
5. In the Setup Dialog use the following values
    - *URL*: The root url / IP of your Beszel instance, like beszel.example.com
    - *user*: Either your default admin username / email or (recommended) create another user with the role user and assigning the agents you want to expose to it.
    - *password*: The password to the user
6. The API will pull the data and reload every 2 minutes

# Usage
After installing the following entities will exposed as sensors (more to come):
- Status (Connection)
- Uptime
- CPU
- Disk usage
- Temperature
- RAM

For example if your machine is named *test*, CPU will be available as ```sensor.test_cpu```