# Use Node.js 16 base image
FROM node:16-bookworm

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install Foundry (todo: specific version)
ENV PATH="/root/.foundry/bin:${PATH}"
RUN curl -L https://foundry.paradigm.xyz | bash
RUN foundryup

# Set working directory
WORKDIR /app

# Clone the repo
# (replace with your actual repo URL)
RUN git clone https://github.com/ArbitrumFoundation/governance.git .

# Optionally, checkout a specific branch or commit
RUN git checkout b98ff9c

RUN git submodule update --init --recursive

# Install dependencies
RUN yarn

# Run your commands (example: build the app)
RUN yarn build

# Default command
ENTRYPOINT ["yarn", "propmon:service"]