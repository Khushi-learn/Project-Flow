# ProjectFlow — Database Design

**Version:** 0.1
**Database:** PostgreSQL

## 1. Design Goals

* Maintain data integrity.
* Represent relationships between users, projects, and tasks.
* Prevent duplicate memberships.
* Support project-level access control.
* Enable efficient filtering and reporting.
* Preserve relevant timestamps and audit information.

## 2. Tables

### users

| Column        | Purpose                                   |
| ------------- | ----------------------------------------- |
| id            | Primary key                               |
| name          | User's display name                       |
| email         | Unique login identifier                   |
| password_hash | Secure password hash                      |
| role          | Administrator, project manager, or member |
| is_active     | Whether the account is active             |
| created_at    | Account creation timestamp                |

### projects

| Column      | Purpose                          |
| ----------- | -------------------------------- |
| id          | Primary key                      |
| name        | Project name                     |
| description | Project description              |
| status      | Active or archived               |
| created_by  | Foreign key referencing users.id |
| due_date    | Optional project deadline        |
| created_at  | Creation timestamp               |
| updated_at  | Last update timestamp            |

### project_memberships

| Column     | Purpose                             |
| ---------- | ----------------------------------- |
| project_id | Foreign key referencing projects.id |
| user_id    | Foreign key referencing users.id    |
| joined_at  | Membership creation timestamp       |

The combination of project_id and user_id forms the composite primary key, preventing duplicate membership records.

### tasks

| Column      | Purpose                                   |
| ----------- | ----------------------------------------- |
| id          | Primary key                               |
| project_id  | Foreign key referencing projects.id       |
| title       | Task title                                |
| description | Task details                              |
| assignee_id | Optional foreign key referencing users.id |
| created_by  | Foreign key referencing users.id          |
| status      | To do, in progress, or done               |
| priority    | Low, medium, or high                      |
| due_date    | Optional deadline                         |
| created_at  | Creation timestamp                        |
| updated_at  | Last update timestamp                     |

### notifications — Future enhancement

| Column     | Purpose                             |
| ---------- | ----------------------------------- |
| id         | Primary key                         |
| user_id    | Foreign key referencing users.id    |
| message    | Notification content                |
| read_at    | Null until the notification is read |
| created_at | Creation timestamp                  |

## 3. Relationships

* One user can create multiple projects.
* Users and projects have a many-to-many relationship through project_memberships.
* One project can contain multiple tasks.
* A task belongs to one project.
* One user can be assigned multiple tasks.
* A task can have no assignee or one assignee.
* One user can receive multiple notifications.

## 4. Constraints

* User email addresses must be unique.
* Required fields must not accept NULL.
* Project membership pairs must be unique.
* Foreign keys must reference valid records.
* Status and priority values must be restricted to supported values.
* A task assignee must be authorized to access the associated project.
* Dates and timestamps must use consistent database types.

The assignee membership rule requires application validation or an appropriate database constraint.

## 5. Indexing Strategy

Potential indexes include:

* users(email)
* projects(created_by, status)
* project_memberships(user_id, project_id)
* tasks(project_id, status)
* tasks(assignee_id, status)
* tasks(due_date)

Indexes will be reviewed against actual query patterns and test data rather than added indiscriminately.

## 6. Deletion and Retention

Projects will initially use an archived status rather than immediate permanent deletion.

Permanent deletion rules, task retention, foreign-key deletion behavior, and backup recovery procedures must be finalized before implementing destructive operations.

## 7. Migrations

Database schema changes will be managed through versioned migrations so that development and production databases can be updated in a controlled manner.

**End of document — Version 0.1**
