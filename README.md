# CircularWood_4.0 Database API

This repository contains the **CircularWood_4.0 Database API**, developed as part of the Circular Wood 4.0 project at the **Robot Lab - Digital Production Research Group - Amsterdam University of Applied Science**.

Contact: j.jooshesh@hva.nl
Javid Jooshesh - Researcher in Robot Lab 

## Project Overview

The primary purpose of the API is to provide a database infrastructure that integrates **design creation**, **material management**, and **production automation**. Here's how the process works:
    <br>
1. **Design and Material Matching**:
    - Users create designs using wood materials from the inventory with the help of a resource matching algorithm. Each design element is stored as a unique record in the database and is **linked to the specific material** selected for use.
    - Nested design elements are referenced to materials in the inventory, ensuring that each piece of material used is tracked back to the produced design it is part of.
    <br>
    
2. **Traceability**:
    - The system ensures full **traceability** of designs and materials. Every design is linked to the user who created it, and the materials used are traceable from stock to production. This ensures transparency and enables resource tracking across the lifecycle of a product.
    - The steps taken in the process from material selection, matching with design, and production are logged as part of the **history** that is related to the materials used. This helps analyze how efficient and sustainable each design and production run is, providing valuable insights for future projects.
    <br>

3. **Automated Production**:
    - Once a design is finalized, the **production files** are generated in a **CAM (Computer-Aided Manufacturing) program**. The way its done is that the CAM program retrieves the **CAD data and design metadata** using the design ID and creates a **production code** that is linked to the materials selected from the inventory.
    - The production code is stored in a **production database**, which enables factory robots to dynamically load and execute the entire production sequence of pickup, sawing, milling profiles, and drop-off of each element after scanning the material at the start of production.
    - This automation is to ensure continuous and efficient production of wood parts linked directly to the specific design and materials.
    <br>

4. **Environmental Impact Tracking**:
    - During the design-to-production process, the system calculates the **saved environmental costs** of using the circular wood compared to using virgin wood using the Idemat database which is used for impact assesment tools.
    - In addition to that, the database stores other information from the production such as the **energy**, **runtime**, and **material costs**.
    - The environmental impact data is calculated in an **Environmental KPI** tool developed in the lab and is stored in the database.

---
### Developer information

#### Requirements

- **Docker**: Ensure Docker is installed on your machine. You can download it from [here](https://www.docker.com/products/docker-desktop).
- **docker-compose**: Use docker-compose to manage and run the api inside a container as service.
- **Python 3.10**: Used for certain setup scripts and database migrations.

---

#### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd circularwood_4.0_api
   ```
   <br>
   
2. **Set up environment**:
    Review and adjust the settings.yml file to suit your environment. Ensure that API port configurations, database connections, and logging levels are set correctly.
    <br>

3. **Build and run the project using Docker for development**:
    `docker-compose up --build`

    This will start the necessary containers, and the API will be available at <http://localhost:5050> (as configured in settings.yml).

---

#### Documentation

For the **API documentation** execute the following script in the terminal:

```bash
$ ./api-docs.sh
```

For the **developer documentation**, execute the following script in the terminal:

```bash
$ ./developer-docs.sh
```

---

#### Configurations

This section provides an overview of the settings available for configuring the CircularWood_4.0 Database API. These configurations allow for easy customization and adaptation to different environments, external services, and security needs.
    <br>
 1. **API Configs such as CORS & Rate Limiting: Control who can access the API and limit requests to prevent overuse.**

    ```yaml
    configs:
        secret_key: 4e5508fd-979d-47ad-a56b-e9a604d02f1f
        propogate_exceptions: true
        rate_limiting:
            requests_per_minute: 100
            burst: 50
        cors:
            access_control_allow_credentials: true
            allow_headers: [ ... ]
            allowed_origins: [ ... ]
        max_content_length: 10485760 # 10MB
    ```
    <br>

 2. **External APIs: Add or modify the URLs of external services like authentication or environmental data APIs.**

    ```yaml
    external:
        apis:
            url:
                - &dev_auth_api_url <http://localhost:1993>
            api_keys: []
        tools:
            idemat:
            path: idemat/idenmat_2023_wood_simplified.json
    ```
    <br>

 3. **Frontend Applications: Update URLs to any frontend applications connected to the API.**

    ```yaml
    frontend_apps:
    url:
        - http://localhost:3000
        - https://robotlab-db-gui.onrender.com
    ```
    <br>

 4. **Server Settings: Adjust the port, host, and environment (development vs. production).**
    ```yaml
    server:
    port: 5050
    host: 0.0.0.0
    environment:
        selected_mode: "development"
        modes: 
        development:
            url: http://localhost:5050
            logging: DEBUG
        production:
            url: https://robotlab-residualwood.onrender.com
            logging: INFO
    ```
    <br>
 5. **Database: Switch from SQLite to a production-ready database like PostgreSQL, MySQL, etc.**
    
    ```yaml
    database:
        server: sqlite
        uri: sqlite:///instance/data.db
        track_modifications: false
    ```
    <br>

 6. **Security: Customize cookie handling and JWT settings to secure your API.**

    ```yaml
    security:

        cookie_settings:
            same_site: 'Strict'
            token_location: "cookies"
            cookie_secure: false
            csrf_in_cookies: false
            http_only: true
            
        jwt:
            secret: "ROBOT-LAB_118944794548470618589981863246285508728"
            issuer: https://robotlab-residualwood.onrender.com
            audience: https://robotlab-residualwood.onrender.com
            expiration_time: 3600
    ```
    <br>

 7. **Logging: Modify the logging format and where logs are written.**

    ```yaml
    logging:
        format: json
        output: stdout
    ```
    <br>

