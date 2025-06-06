FROM node:16-bookworm
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
ENV PATH="/root/.foundry/bin:${PATH}"
RUN curl -L https://foundry.paradigm.xyz | bash
RUN foundryup

WORKDIR /app

RUN git clone https://github.com/ArbitrumFoundation/governance.git .
RUN git checkout b98ff9c
RUN git submodule update --init --recursive
RUN yarn
RUN yarn build

ENTRYPOINT ["yarn", "propmon:service"]