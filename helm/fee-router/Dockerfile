FROM node:22

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
ENV PATH="/root/.foundry/bin:${PATH}"
RUN curl -L https://foundry.paradigm.xyz | bash
RUN foundryup

WORKDIR /app

RUN git clone https://github.com/OffchainLabs/fund-distribution-contracts.git .
RUN git checkout ca792fdae3ed0889ee020be184f9a18c219d4be3

RUN yarn

RUN yarn hardhat compile
RUN forge build

ENTRYPOINT ["yarn"]