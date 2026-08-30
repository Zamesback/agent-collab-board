# Example Project

This is an example project demonstrating basic usage of the multi-agent collaboration board.

## Quick Start

1. Copy the `sample-project` folder to your project root directory (default `~/agent-collab-projects/`)
2. Start the server: `python3 server.py`
3. Open browser: http://localhost:8766
4. Click "sample-project" in the project list to enter the board

## Example Project Contains

- `collab_board.json` — Example board data (4 tasks, 3 messages, 3 agents)
- `project_config.json` — Example configuration (API config, trigger templates)

## Task Status Explanation

| Task | Status | Assignee | Description |
|---|---|---|---|
| T1 Define Project Goals | ✅ Done | User | Example completed task |
| T2 Create Project Plan | 🔄 In Progress | Planner Agent | Example in-progress task |
| T3 Implement Core Features | ⏳ Todo | Unassigned | Example todo task |
| T4 Testing & Acceptance | ⏳ Todo | Unassigned | Example todo task |

## Experience Collaboration Flow

1. Send `@Planner Agent Is the task breakdown done?` in the chat area
2. Click the "Copy Command" button next to the message
3. Paste the copied command into the Planner Agent's chat window
4. After the Planner Agent processes, write the results back to the board
5. Refresh the board page to see the updates

## Customization

- Modify tasks and messages in `collab_board.json`
- Modify agent configuration and trigger templates in `project_config.json`
- Operate directly on the board page (add tasks, send messages, claim tasks)
