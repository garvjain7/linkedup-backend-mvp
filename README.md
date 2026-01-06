# LinkedUp Backend - Social Media Demo App

A command-line social media application built in Python, demonstrating user profiles, posts, reactions, and analytics.

## Features

- **User Management**: Create profiles, login/logout, edit profiles.
- **Posting**: Create and view posts.
- **Interactions**: Like and comment on posts.
- **Analytics**: View user engagement stats.
- **Data Persistence**: Stores data in JSON files.

## Requirements

- Python 3.6+
- No external dependencies (uses standard library only)

## Installation

1. Clone or download the project.
2. Ensure Python 3.x is installed.

## Usage

1. Navigate to the project root.
2. Run: `python main.py`
3. Follow the on-screen menus.

### Menus
- **Guest Menu**: Create Profile, Login, Exit
- **User Menu**: View/Edit Profile, Create Post, React to Posts, View Details, Analytics, Logout, Exit

### Back Options
- Press `0` in input prompts to go back to the previous menu.

## Project Structure

```
linkedUP backend/
├── data/                    # JSON data files
│   ├── posts.json
│   ├── reactions.json
│   └── users.json
├── src/                     # Source code
│   ├── __init__.py
│   ├── app.py               # Main app logic
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # User model
│   └── services/
│       ├── __init__.py
│       ├── analytics_engine.py
│       ├── data_manager.py
│       └── reaction_manager.py
├── main.py                  # Entry point
└── README.md                # This file
```

## Contributing

Feel free to fork and contribute improvements!

## License

MIT License