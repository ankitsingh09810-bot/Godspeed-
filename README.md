Phoenix V100 Nitro is a high-performance, Single-Machine Virtualized Cluster (SMVC) engineered for persistent thread monitoring and automated security. By utilizing asynchronous virtual nodes, the system ensures a "25/7" lock on thread metadata with 5x internal redundancy.

🔱 Core Architecture
The project operates on the Unified Virtualized Cluster (UVC) model. Instead of spawning multiple visible virtual machines, it initializes a single high-performance runner that manages five independent virtual nodes internally.

Stealth Masking: Consolidates 10 parallel threads into a single GitHub Action job to maintain a clean repository history.

5x Internal Redundancy: Five virtual nodes monitor the target thread simultaneously; if one node faces a rate limit, the others remain active.

Resource Optimization: Uses requests for high-speed, low-memory monitoring and asyncio for synchronized execution.

⚙️ Configuration & Setup
1. Repository Secrets

To run the cluster, you must add the following encrypted secrets to your GitHub Repository (Settings > Secrets and Variables > Actions):

Secret	Description
INSTA_COOKIE	Your Session ID (extracted from browser cookies).
TARGET_THREAD_ID	The unique ID of the Direct Message/Group thread.
TARGET_NAME	The specific title or label to be locked and protected.
2. Deployment

Upload bot.py (The Engine) to your root directory.

Upload .github/workflows/phoenix.yml (The Ignitor) to your repository.

The workflow is configured to trigger automatically every 6 hours via cron to provide 24/7 coverage.

⚡ Technical Specifications
Cluster Engine: Python 3.11 with asyncio and requests.

Virtualization: 5 Virtual Nodes with unique simulated User-Agents.

Strike Delay: Staggered CHECK_INTERVAL to prevent simultaneous request spikes.

Persistence: Auto-restart logic ensures the system bypasses the 6-hour GitHub Action timeout.

🔱 Features
SMVC Masking: Hides cluster activity behind a single-job interface.

Nitro Pulse: High-frequency checks (5s interval) for near-instant title reversion.

Automated Maintenance: Wipes VM bloat during setup to maximize RAM for the browser engine.

Disclaimer: This project is for educational purposes and internal thread management. Ensure compliance with platform Terms of Service.

🔱 Developed by Praveer: Titan Guardian Series
