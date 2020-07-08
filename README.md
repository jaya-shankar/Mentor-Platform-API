# Mentor-Platform-API
An API for mentorPlatform website

It's an API I built for the website I creator mentorPlatform
## Build Using
- __djangorestframework__

- __django__

## Working
All the methods and route for the API are given below

Feature | Type | Route | Access
------------ | ------------- | ------------- | -------------
Get all courses | GET | http://127.0.0.1:8000/api/courses | Public
Get a specific course based on id | GET | http://127.0.0.1:8000/api/courses/:id | Public
Get a specific course based on title | GET | http://127.0.0.1:8000/api/courses/title/:title| Public
Create a course | POST | http://127.0.0.1:8000/api/courses | Protected
Update a specific course | PUT | http://127.0.0.1:8000/api/courses/:id  http://127.0.0.1:8000/api/courses/title/:title  | Protected
Delete a specific course | DELETE | http://127.0.0.1:8000/api/courses/:id  http://127.0.0.1:8000/api/courses/title/:title | Protected
Get all messages from a specific course | GET | http://127.0.0.1:8000/api/courses/:id/messages  http://127.0.0.1:8000/api/courses/title/:title/messages | Protected
Send a message in a specific course | POST | http://127.0.0.1:8000/api/courses/:id/messages  http://127.0.0.1:8000/api/courses/title/:title/messages | Protected
Get all doubts of a specific course | GET | http://127.0.0.1:8000/api/courses/:id/doubts http://127.0.0.1:8000/api/courses/title/:title/doubts | Protected
Send a doubt to a specific course | POST | http://127.0.0.1:8000/api/courses/:id/doubts http://127.0.0.1:8000/api/courses/title/:title/doubts | Protected
Get all users | GET | http://127.0.0.1:8000/api/users | Public
Add a new User | POST | http://127.0.0.1:8000/api/users | Public
Get a specific user based on id | GET | http://127.0.0.1:8000/api/users/:id | Public
Get a specific user based on username | GET | http://127.0.0.1:8000/api/users/username/:username | Public
Update a specific User | PUT | http://127.0.0.1:8000/api/users/username/:username http://127.0.0.1:8000/api/users/username/:username | Protected
Delete a specific User | DELETE | http://127.0.0.1:8000/api/users/username/:username http://127.0.0.1:8000/api/users/username/:username | Protected
Get all doubts asked by a specific user | GET |http://127.0.0.1:8000/api/users/:id/doubts  http://127.0.0.1:8000/api/users/username/:username/doubts | Public
Authenticate a user | POST | http://127.0.0.1:8000/api/auth | Public


