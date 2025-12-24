#!/bin/bash

set -ex

# Update and Install dependencies
apt-get update -y
apt-get install -y docker.io docker-compose git

# Add the current user to the docker group
usermod -aG docker $(whoami)

# Start and enable Docker
systemctl start docker
systemctl enable docker

# Clone the repository
if [ -n "${repo_url}" ]; then
  # Use the token to clone the private/public repo
  git clone "https://${gh_pat}@github.com/TARIFUDDIN/Aero-Bound-Ventures-Public.git"

  # Create the .env file inside the CORRECT folder (Hardcoded 'backend')
  cat <<EOF > Aero-Bound-Ventures-Public/backend/.env
MAIL_USERNAME=${mail_username}
MAIL_PASSWORD=${mail_password}
MAIL_FROM=${mail_from}
MAIL_PORT=${mail_port}
MAIL_SERVER=${mail_server}
ACCESS_TOKEN_EXPIRE_MINUTES=${access_token_expire_minutes}
SECRET_KEY=${secret_key}
ALGORITHM=${algorithm}
AMADEUS_API_KEY=${amadeus_api_key}
AMADEUS_API_SECRET=${amadeus_api_secret}
AMADEUS_BASE_URL=${amadeus_base_url}
DATABASE_URL=${database_url}
PESAPAL_CONSUMER_KEY=${pesapal_consumer_key}
PESAPAL_CONSUMER_SECRET=${pesapal_consumer_secret}
PESAPAL_BASE_URL=${pesapal_base_url}
PESAPAL_IPN_ID=${pesapal_ipn_id}
EOF

  # Go to the CORRECT folder and start Docker (Hardcoded 'backend')
  cd Aero-Bound-Ventures-Public/backend
  docker-compose up -d --build
fi