# Finalization Abstract (Making of)

GitHub repository link: `https://github.com/<user_name>/<repository_name>`

This project delivers a complete Python backend for a habit tracking application focused on the essential requirements of the assignment. The application lets users create multiple habits, track completion events over time, and analyse streak performance across daily and weekly periodicities.

The technical approach combines object-oriented and functional programming. The `Habit` model represents the core OOP entity and captures metadata such as creation timestamp, periodicity, and description. Persistent storage is implemented with SQLite to ensure data is retained between sessions. A repository class encapsulates all database interactions, making the system easier to maintain and test.

A command-line interface was implemented as the public API. It supports database setup, fixture loading, habit creation/deletion, check-off actions, and analytics queries. This keeps usage simple and transparent while meeting the requirement of a clean user-facing interface.

A major part of the project was designing analytics with functional techniques. The analytics module computes filtered habit lists and streak values using composable functions and immutable-style transformations on completion timestamps. This includes the longest streak per habit and the longest streak across all habits.

To validate functionality, the project includes an automated unit test suite with pytest. Fixtures include five predefined habits (with both daily and weekly habits) and four weeks of completion data, which supports deterministic tests and demonstrations.

Overall, the project meets the acceptance criteria with a practical, extensible architecture. The strongest aspect is the clear separation between domain logic, persistence, analytics, and interface. A future extension could add a web UI and user authentication without changing the core tracking engine.
