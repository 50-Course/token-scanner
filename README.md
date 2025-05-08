# token-scanner

[![CI](https://github.com/50-Course/token-scanner/actions/workflows/ci.yml/badge.svg)](https://github.com/50-Course/token-scanner/actions/workflows/ci.yml)

> UPDATE (May 8 '25 19:34): I have just received important notification an hour ago that the server running
> this application had been shutdown due to billing issue - as a temporary
> measure, I have redeployed out here on:
>
> Host: [https://token-scanner-2y31.onrender.com](https://token-scanner-2y31.onrender.com). Please change host accordingly.
>
> Hence, new [API Docs](https://token-scanner-2y31.onrender.com/api/docs)

API Reference: [API Docs](http://104.154.104.188:8000/api/docs)

OpenAPI Playground (Swagger): [Playground](http://104.154.104.188:8000) or [![Try it Now in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/17035192-27110b7f-d1b7-4dff-af3f-afc32f51df00?action=collection%2Ffork&collection-url=entityId%3D17035192-27110b7f-d1b7-4dff-af3f-afc32f51df00%26entityType%3Dcollection%26workspaceId%3D180d64b0-8c9d-4eb1-9d1a-ead38ec6a1a8)

The Night Watch Guild for Crypto Transactions on the Ethereum, Solana, and
Binance Smart Chain networks.

![image](https://github.com/user-attachments/assets/d15b2ca8-cf52-46aa-acfe-f114633ea449)

## Architecture

### Decisions

> Imagine a world where we can scan the blockchain for transactions and expose
> those transactions to the world in a way that is easy to understand and useful
> for on-chain analysis. This is the goal of the Night Watch Guild.

- Follows REST architecture
- Fast (~2s response time)
- Simple, initutive interface for Querying Data (GET)
- Fully containerized using Docker
- And, Bootstrapped using Docker Compose

### System Design

**The Architecture**

Token Scanner is designed to be a simple and efficient way to scan the
blockchain for transactions. It provides a single API endpoint that allows
users to scan a blockchain for transactions. At the moment, only three on-chain
scans are permitted; `Ethereum`, `Solana` and `Binance Smart Chain` (ongoing support/development).

```mermaid
graph TD
    A[User] -->|GET| B[API]
    B -->|GET| C[TokenScanner]
    C -->|GET| D[Ethereum]
    C -->|GET| E[Solana]
    C -->|GET| F[BinanceSmartChain]
```

**Proposed API Design**

Below is the proposed API design for the Night Watch Guild. The API will provide endpoints for scanning the blockchain and retrieving transactions.

Resource URI: `/api/v1/tokens/pools`

- Method: `GET`

Example Request:

```bash
  curl -sSL http://localhost:8000/api/v1/tokens/pools?chain_id=solana&token_addresses=ADDRESS1,ADDRESS2
```

**Relationship diagram**

```mermaid
erDiagram
    Token ||--o{ Pool : "pools"
    Token }o--|| Pool : "largest_pool"
    Pool }o--|| Token : "token"
```

### How It Works

1. The user sends a request to the API to scan the blockchain for transactions.
2. The API calls the appropriate blockchain scanner (Ethereum, Solana, or
   Binance Smart Chain) to scan the blockchain.
3. The scanner scans the blockchain and returns the transactions to the API.

## Usage

The API is accessible through any client, perhaps you are the terminal guy on a sunny evening - feel free to make a request as below:

```sh
curl --location --request GET 'http://104.154.104.188:8000/api/v1/tokens/pools?addresses=FQgtfugBdpFN7PZ6NdPrZpVLDBrPGxXesi4gVu3vErhY&chain_id=solana'
```

Or you more confortable with GUI's please, access the API via your favorite API test client. For example below is another example:

![image](https://github.com/user-attachments/assets/a596ba41-bbd6-4884-b94f-5ef39f075a3d)

See the API Docs, for information on how to configure the right parameters.

You may also spin up a local copy of the reposistory to have everything right on your system. For more information, follow the below guide to hit the ground up and running.

### Prerequisites

- Docker
- Docker Compose
- Python 3.12 or higher
- Poetry

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/50-Course/token-scanner.git

    cd token-scanner
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Before you build and run the Docker containers, copy the template environment variables and set it appropriately:

   ```bash
    cp tokenscanner/.env.template tokenscanner/src/.env

    docker-compose up --build
   ```

4. Access the API at `http://localhost:8000/api/v1/tokens/pools` (local).
5. Use the API to scan the blockchain for transactions. See the [API documentation](http://104.154.104.188:8000/api/docs) for more details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the Apache-2.0 License - see the [LICENSE](LICENSE) file for details.
