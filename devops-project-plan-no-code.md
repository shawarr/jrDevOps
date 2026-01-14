# DevOps Beginner Project: Build & Deploy a Web App

## Learn by Doing — Guidance Without Hand-Holding

---

## 🎯 The Project

**Build a simple "Status Dashboard" API and deploy it with a full DevOps pipeline.**

By the end, you'll have:

- A working application running in the cloud
- Automated deployments (push code → automatically deploys)
- Monitoring and health checks
- Infrastructure defined as code
- A portfolio piece to show employers

---

## The Philosophy

This guide tells you **what** to do and **why**, but not **how**. You'll need to:

- Google things
- Read documentation
- Try, fail, and try again
- Understand what you're doing, not just copy commands

This is how real DevOps engineers work every day.

---

## Prerequisites

Before starting, install these on your computer:

1. **A code editor** (VS Code is popular)
2. **Git** (search "install git" for your OS)
3. **Docker Desktop** (for Mac/Windows) or Docker Engine (for Linux)
4. **Python 3.11+**
5. **A GitHub account** (free)
6. **An AWS account** (free tier is enough)

---

## Step 1: Create the Application

**Goal:** Have something to deploy
**Time:** 1-2 hours

### What to Build

A minimal Flask API with these endpoints:

- `GET /` — Returns a welcome message
- `GET /health` — Returns health status (monitoring tools will hit this)
- `GET /info` — Returns app version, hostname, environment (useful for debugging deployments)
- `GET /ready` — Returns readiness status

### Tips

- Keep it dead simple — you're learning DevOps, not web development
- The `/health` endpoint is important — you'll use it later for monitoring and CI/CD checks
- The `/info` endpoint should read from environment variables so you can change values without changing code
- Use `socket.gethostname()` in `/info` — it'll show something interesting when containerized
- Create a `requirements.txt` file listing your dependencies

### What to Google

- "Flask minimal API example"
- "Flask return JSON response"
- "Python read environment variable"
- "Python requirements.txt"

### Checkpoint

✅ Run your app locally and hit all endpoints in your browser. See JSON responses? Move on.

---

## Step 2: Initialize Git Repository

**Goal:** Version control your code
**Time:** 30 minutes

### What to Do

1. Create a `.gitignore` file appropriate for Python projects
2. Initialize a git repository in your project folder
3. Make your first commit
4. Create a new repository on GitHub
5. Connect your local repo to GitHub and push

### Tips

- Never commit sensitive files (`.env`, credentials, etc.) — that's what `.gitignore` is for
- Your commit messages should describe what changed
- GitHub will show you the commands to connect an existing repo when you create an empty one

### What to Google

- "Python .gitignore template"
- "Git init and first commit"
- "Connect local repo to GitHub"

### Checkpoint

✅ Your code appears on GitHub? Move on.

---

## Step 3: Containerize with Docker

**Goal:** Package your app so it runs the same everywhere
**Time:** 1-2 hours

### What to Do

1. Create a `Dockerfile` that:

   - Starts from a Python base image
   - Copies your code into the container
   - Installs dependencies
   - Exposes the right port
   - Runs your app with a production server (not Flask's dev server)

2. Create a `docker-compose.yml` for easy local development

3. Build your image and run it

### Tips

- Use a "slim" base image to keep size small
- Copy `requirements.txt` and install dependencies BEFORE copying the rest of your code — this improves build caching
- Flask's built-in server is for development only. Research `gunicorn` for production
- When your app runs in a container, the hostname will be the container ID — that's why `/info` is useful
- Don't run as root inside containers (research why this matters for security)

### What to Google

- "Dockerfile Python Flask example"
- "Docker best practices Python"
- "Gunicorn Flask production"
- "docker-compose basics"
- "Docker build and run commands"

### Checkpoint

✅ App runs in Docker, you can hit `http://localhost:5000/info` and see a container ID as hostname? Commit and push, then move on.

---

## Step 4: Add CI/CD Pipeline

**Goal:** Automate testing and building on every push
**Time:** 2-3 hours

### What to Do

1. Create a GitHub Actions workflow file (lives in `.github/workflows/`)

2. Your pipeline should have these jobs:

   - **Test:** Set up Python, install dependencies, run tests
   - **Build:** Build Docker image, verify container starts and responds to health checks
   - **Deploy:** (Placeholder for now) Just echo a message

3. Write a few basic tests for your endpoints using `pytest`

### Tips

- GitHub Actions uses YAML — indentation matters a lot
- Jobs can depend on other jobs using `needs`
- Use `if` conditions to control when jobs run (e.g., only deploy on push to main, not on PRs)
- Your build job should actually start the container and `curl` the health endpoint to verify it works
- Start simple and add complexity gradually

### What to Google

- "GitHub Actions Python workflow"
- "GitHub Actions Docker build"
- "Pytest Flask testing"
- "GitHub Actions job dependencies"
- "GitHub Actions run only on main branch"

### Checkpoint

✅ Push code, go to Actions tab, see green checkmarks? Write a test that fails, push, see red X? Fix it, push, green again? Move on.

---

## Step 5: Deploy to AWS EC2

**Goal:** Get your app running on a real server on the internet
**Time:** 3-4 hours

This is where things get real. Expect to troubleshoot.

### What to Do

**5.1 Launch an EC2 Instance:**

- Use Ubuntu Server (latest LTS version)
- Instance type: t2.micro (free tier eligible)
- Create and download a key pair (you'll need this to SSH in)
- Configure security group to allow:
  - SSH (port 22)
  - Your app port (5000)
  - HTTP (port 80) for later

**5.2 Connect to Your Server:**

- SSH into your instance using the key pair

**5.3 Set Up the Server:**

- Update the system packages
- Install Docker
- Configure Docker to start on boot
- Add your user to the docker group (so you don't need sudo)

**5.4 Deploy Your App:**

- Clone your repository from GitHub
- Build and run your Docker container
- Test it works via the public IP

### Tips

- Your `.pem` key file needs specific permissions or SSH will refuse to use it
- After adding yourself to the docker group, you need to log out and back in
- Security groups are like firewalls — if you can't connect, check there first
- EC2 instances have both public and private IPs — use the public one
- The instance needs outbound internet access to clone from GitHub

### What to Google

- "Launch EC2 instance step by step"
- "SSH into EC2 Ubuntu"
- "Install Docker on Ubuntu 24.04"
- "EC2 security group configuration"
- "Permission denied publickey EC2"

### Checkpoint

✅ Open `http://YOUR_EC2_PUBLIC_IP:5000` in your browser and see your app? Congratulations, you've deployed to the cloud! Move on.

---

## Step 6: Automate Deployment

**Goal:** Push to GitHub → App automatically updates on server
**Time:** 2-3 hours

### What to Do

**6.1 Create a Deployment Script on the Server:**

- Write a bash script that:
  - Pulls the latest code from GitHub
  - Rebuilds the Docker image
  - Stops and removes the old container
  - Starts a new container
- Make it executable
- Test it manually

**6.2 Connect GitHub Actions to Your Server:**

- Store your EC2 SSH key as a GitHub secret
- Store your EC2 host IP as a GitHub secret
- Update your GitHub Actions deploy job to:
  - SSH into your server
  - Run deployment commands

### Tips

- GitHub Secrets are found in repo Settings → Secrets and variables → Actions
- There are pre-built GitHub Actions for SSH (search for them in the marketplace)
- Your bash script should handle the case where no container is running yet (hint: `|| true`)
- Use `--restart unless-stopped` when running your container so it survives server reboots
- Test by making a small change to your app, push, and verify it updates automatically

### What to Google

- "Bash script basics"
- "GitHub Actions SSH to server"
- "GitHub Actions secrets"
- "Docker restart policy"
- "GitHub Actions marketplace SSH"

### Checkpoint

✅ Change something in your app, push to main, wait for Actions to complete, refresh your EC2 URL and see the change? Move on.

---

## Step 7: Add Monitoring

**Goal:** Know when your app is down before users tell you
**Time:** 1-2 hours

### What to Do

**7.1 External Uptime Monitoring:**

- Sign up for a free uptime monitoring service (UptimeRobot, Better Uptime, etc.)
- Add a monitor pointing to your `/health` endpoint
- Configure email alerts

**7.2 Add Logging to Your App:**

- Use Python's built-in logging module
- Log important events (requests, errors, startup)
- Learn to view Docker container logs on the server

### Tips

- Your `/health` endpoint is specifically for monitoring tools to ping
- Most uptime services have a free tier that's enough for personal projects
- Structured logging becomes important at scale, but basic logging is fine to start
- `docker logs` with `-f` flag follows logs in real-time (like `tail -f`)
- Consider what happens when your app crashes — will the container restart automatically?

### What to Google

- "Free uptime monitoring services"
- "Python logging best practices"
- "Docker logs command"
- "Docker container restart automatically"

### Checkpoint

✅ Stop your container manually, receive an alert email, start it again, get "back up" notification? Move on.

---

## Step 8: Infrastructure as Code with Terraform

**Goal:** Define your infrastructure in code, not clicks
**Time:** 3-4 hours

### What to Do

**8.1 Install and Configure:**

- Install Terraform locally
- Install AWS CLI and configure it with your credentials

**8.2 Write Terraform Configuration:**
Create files that define:

- A security group with the right ports open
- An EC2 instance with:
  - The right AMI (Ubuntu)
  - The right instance type
  - The security group attached
  - User data script to install Docker on first boot
- Output values (public IP, instance ID, app URL)

**8.3 Use Terraform:**

- Initialize Terraform in your directory
- Run plan to see what will be created
- Apply to create the infrastructure
- Verify it works
- Destroy when done (to avoid charges)

### Tips

- Terraform uses its own language (HCL) — it's not that hard but has a learning curve
- `terraform plan` shows what WILL happen without doing it — always run this first
- State files (`.tfstate`) are important — don't delete them, and don't commit them to git
- Use variables for things that might change (region, instance type, AMI ID)
- The AMI ID is different in each AWS region — find the right one for your region
- User data scripts run as root on first boot — useful for initial setup

### What to Google

- "Install Terraform"
- "Configure AWS CLI credentials"
- "Terraform AWS EC2 example"
- "Terraform variables"
- "Terraform user data"
- "Ubuntu AMI ID [your region]"
- "Terraform state file"

### Checkpoint

✅ Run `terraform apply`, wait for EC2 to launch, SSH in and verify Docker is installed, then `terraform destroy` and watch it all disappear? You've completed the project!

---

## 🎉 Project Complete!

### Skills You've Practiced

| Skill           | How You Used It                                                |
| --------------- | -------------------------------------------------------------- |
| Linux           | SSH, file permissions, package management, services            |
| Git             | Init, commit, push, branches, remote repos                     |
| Docker          | Dockerfile, images, containers, compose, registries            |
| CI/CD           | GitHub Actions, pipelines, jobs, secrets, automated deployment |
| AWS             | EC2, security groups, key pairs, networking                    |
| Monitoring      | Health checks, uptime monitoring, logging                      |
| IaC             | Terraform, HCL, state management, infrastructure automation    |
| Troubleshooting | All the things that broke along the way                        |

---

## What's Next?

Once comfortable, explore:

1. **Add a database** — PostgreSQL in a container or AWS RDS
2. **Use a container registry** — Push images to Docker Hub or AWS ECR
3. **Add nginx** — Reverse proxy, serve on port 80
4. **HTTPS** — Get a domain, set up SSL with Let's Encrypt
5. **Kubernetes** — Try minikube locally, then EKS
6. **Better monitoring** — Prometheus + Grafana stack
7. **Configuration management** — Ansible for server setup

---

## When You Get Stuck

1. **Read the error message carefully** — it usually tells you what's wrong
2. **Google the exact error** — someone else has had this problem
3. **Check the basics:**
   - Are you in the right directory?
   - Is the service running?
   - Is the port open?
   - Are the permissions correct?
4. **Check logs** — application logs, Docker logs, system logs
5. **Simplify** — if something complex isn't working, try a simpler version
6. **Take a break** — fresh eyes solve problems faster

---

## Time Estimate

| Step                | Estimated Time   |
| ------------------- | ---------------- |
| Step 1: Create App  | 1-2 hours        |
| Step 2: Git Setup   | 30 min           |
| Step 3: Docker      | 1-2 hours        |
| Step 4: CI/CD       | 2-3 hours        |
| Step 5: AWS Deploy  | 3-4 hours        |
| Step 6: Auto Deploy | 2-3 hours        |
| Step 7: Monitoring  | 1-2 hours        |
| Step 8: Terraform   | 3-4 hours        |
| **Total**           | **~15-20 hours** |

This estimate assumes a lot of Googling and troubleshooting. That's normal. That's the job.

---

## Final Advice

- **Don't skip steps** — each builds on the last
- **Commit often** — small, working increments
- **Break things on purpose** — then fix them (best way to learn)
- **Document what you learn** — future you will thank present you
- **It's okay to struggle** — that's where learning happens

Every error you encounter is a learning opportunity. Every problem you solve is a skill you've gained.

Good luck!
