# Upstox Integration Python


## Project Overview
This project aims to integrate **Upstox API** into Python project for streamlined access to **stock market data**, trading operations, and portfolio management.
This Python project demonstrates how to connect to the **Upstox Websocket API** for streaming **live market data**.

Leverage **Upstox Developer APIs** in your Python project to access market insights.

This project analyze the CandleStick Pattern like:
* **Hammer**
* **Inverted Hammer**
* **Doji**
* **Spinning Top or Bottom**


## Installation

#### Prerequisites
* Python 3.8 or Later
* Upstox Demat Account

## Steps

1. Create App in Upstox Demat Account. Copy Client ID and Client Secret from created App.

    Steps for Create App on Upstox -
[Create App Steps](https://help.upstox.com/support/solutions/articles/258159-how-to-create-an-api-app-)


2. Clone the repository:
    ```bash
    git clone https://github.com/username/repository.git
    cd repository
    ```

3. Create Virtual Environment
    ```
    python -m venv venv
    ```

4. Activate the Virtual Environment:

    * On Windows:

        ```bash
        venv\Scripts\activate
        ```

    * On Mac or Linux:

        ```bash
        source venv/bin/activate
        ```

5. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

6. Add .env file for configuration and add below:

    ```bash
    API_KEY=<your_client_id>
    API_SECRET=<your_client_secret>
    REDIRECT_URL=<redirect_url>
    ```

## Data and Reports

After Filtering the CandleStick, the application creates a individual CSV files for Hammer and Doji in the system.

Two Files:
 - A CSV file contains Stock names with Hammer
 - A CSV file contains stock names with Doji
 - A CSV file contains stock name with Inverted Hammer
 - A CSV file contains stock name with Spinning Top and Bottom


## Acknowledgements

We would like to thank the following resources and libraries that made this project possible:

* **Upstox**: for providing the APIs and resources that enabled the development of this project.
* **Python Decouple**: A tool to manage settings and environment variables, enabling easy configuration of the project.
* **Open Source Community**: For providing valuable resources, libraries, and tools that aid in the development of web applications.
