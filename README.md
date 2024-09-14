# Project Assignments Portal

- [Built With](#built-with)
- [Getting Started](#1-getting-started)
- [Prerequisites](#12-prerequisites)
- [Optional Tools](#121-optional-tools)
- [Installation](#13-installation)
- [Environment](#14-environment)
- [Database](#15-database)
- [Database Init](#151-database-init-fresh-install-only)
- [Running Locally](#2-running-locally)
- [Running the API & UI Separately](#21-running-the-api-and-ui-separately-optional)
- [Accessing the Application](#22-accessing-the-application)
- [Deployment](#3-deployment)
- [Author](#author)
- [License](#license)

A full-stack web application for the management of team project assignments, customers and team members. The backend is written in Python and the UI is built using TypeScript.
This application is developed to be deployed on [Vercel](http://vercel.com), utilizing vercel serverless python functions for the backend and the [NextJS](https://nextjs.org/) framework for the UI. The application uses a PostgreSQL database and the [SQLAlchemy 2.0](https://www.sqlalchemy.org/) ORM, the database also resides on Vercel although it is easily changeable.

## Built With

- [FastAPI](https://fastapi.tiangolo.com/) - API framework
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/) - Database ORM
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) - Database Migration Tool
- [React](https://react.dev/) - UI Library
- [NextJS](https://react.dev/) - React Framework
- [ShadCN](https://ui.shadcn.com/) - UI Component Library
- [Tailwind CSS](https://tailwindcss.com/) - CSS Framework
- [Vercel](https://vercel.com/) - Cloud Platform

## 1. Getting Started

This section will get you started with setting up the codebase locally for development. See [Deployment](#3-deployment) section for notes on how to deploy the project.

### 1.2. Prerequisites

What things you need to install the software and how to install them

- Base requirements
  - [Alembic 1.13.2+](https://alembic.sqlalchemy.org/)
  - [Python 3.12.+](https://www.python.org/)
  - [Node.js v20.x](https://nodejs.org/en/)
  - [pnpm v9.9.0](https://pnpm.io/)

### 1.2.1 Optional Tools

- Additional requirements
  - [Vercel CLI](https://vercel.com/docs/cli)

### 1.3. Installation

Install all UI dependencies and create a Python virtual environment, from the root directory run:

```bash
pnpm initial-setup
```

Once complete, activate the virtual environment:

```bash
source .venv/bin/activate
```

Now all Python dependencies can be installed:

```bash
pnpm api:install-dev
```

### 1.4. Environment

- Have a look at [.env.example](.env.example).
- Copy the example to a new file called .env:

```bash
cp .env.example .env
```

- Make sure the environment variables are entered:
  - The postgres database url
  - The JWT secret

### 1.5. Database

- Technologies used
  - [Alembic 1.13.2+](https://alembic.sqlalchemy.org/)
  - [Vercel Postgres](https://vercel.com/docs/storage/vercel-postgres)
  - [asyncpg](https://magicstack.github.io/asyncpg/current/)

Alembic is the tool used by this project for database migrations.

#### 1.5.1 Database Init (Fresh Install Only)

If this is a fresh install and deployment a new database migration will be needed. This will create the tables and data models in your postgresql database.

Make sure that you remove the [.versions/](./alembic/versions/) directory first:

```bash
rm -rf ./alembic/versions
```

Then run:

```bash
alembic revision --autogenerate -m "initial db config"
```

This will generate a migration file, to then update your database run:

```bash
alembic upgrade head
```

To create a new migration run:

```bash
alembic revision --autogenerate -m "<description of change>"
```

To deploy the migration to the database:

```bash
alembic upgrade head
```

This project has only been configured and tested using a Vercel postgresql database, if you are attempting to deploy onto an alternative database make sure you adjust the configuration appropriately.

## 2. Running Locally

The app can now be run locally. It is possible to run the app in one terminal by simply running the following command from the project root:

```bash
pnpm dev
```

### 2.1. Running the API and UI separately (optional)

To run the backend and frontend in separate terminals, in the project root, run the following commands in separate terminals:

```bash
pnpm api:dev
```

```bash
pnpm ui:dev
```

### 2.2. Accessing the application

By default, the UI can be accessed locally by visiting <http://localhost:3000>

- The UI will run on port 3000 and the backend on port 8000.
- You will see a log in screen. You will need to first create an account:
  - Create an account, make sure to select role: 'MANAGER' - this generates an admin account.
  - On creation you will be logged in to the application.
  - You can now:
    - Create, update and delete Customers.
    - Create, update and delete Projects.
      - (A Project had to be associated with a Customer)
    - Assign / Unassign team members from projects.
    - Edit your own profile.
- A general user ('ENGINEER') account only has read access - they cannot create / update / delete any entities. They can update their own user profile.

## 3. Deployment

To deploy on Vercel you will need an account set up. Vercel can be configured so a deployment runs automatically whenever a change is pushed to the associated GitHub. The [vercel.json](./vercel.json) file contains the necessary config for the deployment to Vercel.

It is also possible to deploy to vercel from the CLI by installing and running the [Vercel CLI](https://vercel.com/docs/cli) tool.

By deploying the application on Vercel, the Python backend will be deployed onto a serverless Python function. The UI will be a combination of bundled static pages and a NodeJS serverless function. These services are fully managed by Vercel.

## Author

- **Ashley Taylor** - _Initial work_ - [PurpleBooth](https://github.com/PurpleBooth)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
