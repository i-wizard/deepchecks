# Deep Checks LLM
This repository holds the  `backend api` source code Deep Checks LLM module.
## STEPS TO RUN PROJECT

Clone project from GitHub to local directory
```bash
git clone git@github.com:i-wizard/deepchecks.git
```
Change directory to project root
```bash
cd deepchecks
```
Create and populate  a local .env file
```bash
pbcopy < sample.env && pbpaste > .env
```
Run project (Ensure you have docker installed on your machine)
```bash
docker compose up
```
Stop all running containers
```bash
docker compose down
```
Build new app image
```bash
docker compose build
```
### View Project
Visit http://localhost:8001/docs/ as the API playground (interface) to view and test API endpoints
You can use the `sample.csv` file located in the `root` folder of this repo to test the csv upload endpoint

### View Mongo db via dashboard
Visit  http://localhost:7000
#### Login credentials
username: user
password: password