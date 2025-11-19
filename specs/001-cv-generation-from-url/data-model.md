# Data Model

This document defines the core data entities for the application.

## 1. Job

Represents the details of a job vacancy extracted from a URL.

| Field           | Type     | Description                                       | Example                               |
|-----------------|----------|---------------------------------------------------|---------------------------------------|
| `id`            | `string` | Unique identifier (e.g., hash of the URL)         | `abc123def456`                        |
| `url`           | `string` | The URL of the job posting.                       | `https://linkedin.com/jobs/view/123`  |
| `title`         | `string` | The job title.                                    | `Software Engineer`                   |
| `company`       | `string` | The name of the company.                          | `Tech Corp`                           |
| `description`   | `string` | The full description of the job.                  | `Looking for a proactive developer...`|
| `skills`        | `array`  | A list of skills required for the job.            | `["Python", "React", "SQL"]`          |
| `createdAt`     | `date`   | Timestamp of when the job was first processed.    | `2025-11-19T10:00:00Z`                |

## 2. GeneratedAssets

Represents the set of materials generated for a specific job application.

| Field           | Type     | Description                                       |
|-----------------|----------|---------------------------------------------------|
| `jobId`         | `string` | Foreign key referencing the `Job` entity.         |
| `cv`            | `string` | The generated, tailored CV content (Markdown/Text).|
| `coverLetter`   | `string` | The generated cover letter content.               |
| `networking`    | `string` | Networking tips and potential contacts.           |
| `insights`      | `string` | Actionable tips and insights about the application.|
| `matchScore`    | `number` | A score from 0 to 100 indicating the match quality.|
| `generatedAt`   | `date`   | Timestamp of when the assets were generated.      |

## 3. ApplicationHistory

Represents an entry in the user's local application history. This will be stored in IndexedDB.

| Field           | Type     | Description                                       |
|-----------------|----------|---------------------------------------------------|
| `id`            | `string` | Unique identifier for the history entry.          |
| `jobTitle`      | `string` | The title of the job applied for.                 |
| `companyName`   | `string` | The name of the company.                          |
| `applicationDate`| `date`  | The date the user generated the materials.        |
| `jobUrl`        | `string` | The original URL of the job posting.              |
| `generatedAssetsId`| `string`| A reference to the generated assets.           |
