# Tarea3_PCD
Manage a client database through a API


### How to run the app:
In order to install the dependencies used for this project you need to run in your terminal: 
```bash
   uv sync
   ```
After that, because the API is protected with a key, you have to create a **.env** file following the structure of the **.env.example** where you are gonna declare the API Key.

And then you run:
```bash
   uv run fastapi dev main.py
   ```

Which will automatically pop up a window with the home page of the API.

---
The Api consist of 4 endpoints:

The structure of the user is:

```json
{
  "user_name": "string",
  "user_email": "user@example.com",
  "age": 19,
  "recommendations": [
    "string"
  ],
  "zip": "string"
}
```

##### GET

Returns all the existing users

For example, in mine it gives: 

```json
[
  {
    "recommendations": [
      "Cidade de Deus",
      "Good Will Hunting",
      "Ran"
    ],
    "age": 20,
    "user_email": "funkysalmon864@outlook.com",
    "user_id": 1,
    "user_name": "FunkySalmon0105",
    "zip": "45116"
  },
  {
    "recommendations": [
      "Batman",
      "The Godfather",
      "When Harry Met Sally"
    ],
    "age": 19,
    "user_email": "rafaeltakata0105@gmail.com",
    "user_id": 2,
    "user_name": "RafaelTakata0105",
    "zip": "32567"
  }
]
```

##### GET with id

Returns just the body of the user that matches the id, if it does not find the id, it gives an error.


##### POST

Creates a new user given the body and the parameters. It only accepts email types and unique values there. So it will not accept a duplicate in email. Remember to follow the structure.

##### PUT

Given the body and user_id changes the old data to the new gived. This won't work if the id does not exist or the new email that you are trying to write is already taken.

##### DELETE

Deletes the user corresponding to the matching ID


