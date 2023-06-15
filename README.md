# postEditApp
Demo link: https://www.youtube.com/watch?v=Ag0X3o8nUJ8
Title: Implementation Description of a Web Application with Actions and APIs


 Add Post Action:
- The `addpost` action handles the addition of a new post.
- It creates a form using the `Form` class and renders the 'add.html' template.
- If the form is accepted (submitted), the data is saved to the database, and the user is redirected to the homepage.

Edit Post Action:
- The `editpost` action is responsible for editing an existing post.
- It retrieves the post from the database based on the provided `post_id` parameter.
- If the post exists, a form is created using the `Form` class and pre-populated with the post data.
- If the form is accepted (submitted), the changes are saved to the database, and the user is redirected to the homepage.

Delete Post Action:
- The `deletepost` action handles the deletion of a post.
- It retrieves the post based on the provided `post_id` parameter and deletes it from the database.
- After deletion, the user is redirected to the homepage.

Load Contacts API:
- The `load_contacts` API retrieves contact records from the database and returns them as a dictionary.
- The `db` object is used to query the 'contact' table and fetch all rows.
- The rows are converted to a list of dictionaries and returned as the API response.

Add Contact API:
- The `add_contact` API adds a new contact record to the database.
- The current user's first name is retrieved using the `auth.current_user` object.
- The contact data is extracted from the JSON payload received in the request.
- The contact record is inserted into the

 'contact' table using the `db.contact.insert` method.
- The selected color is stored in the session for future reference.
- The contact ID and the current user's first name are returned as the API response.

Delete Contact API:
- The `delete_contact` API deletes a contact record from the database based on the provided contact ID.
- The contact ID is extracted from the request parameters.
- The corresponding contact record is deleted using the `db` object.
- A simple 'ok' string is returned as the API response.

Edit Contact API:
- The `edit_contact` API updates a contact record in the database.
- The contact ID, field, and value are extracted from the JSON payload in the request.
- The `db` object is used to update the contact record with the provided field and value.
- If the field being updated is 'color', the selected color is stored in the session.
- A delay of 1 second is added to simulate processing time (for debugging purposes).
- An 'ok' string is returned as the API response.

Upload Thumbnail API:
- The `upload_thumbnail` API updates the thumbnail field of a contact record in the database.
- The contact ID and thumbnail URL are extracted from the JSON payload.
- The `db` object is used to update the contact record with the provided thumbnail URL.
- An 'ok' string is returned as the API response.

Set Follow API:
- The `set_follow` API manages the following functionality between users.
- The user ID to follow and the follow status are extracted from the JSON payload.
- If follow is true, a new record is inserted into the 'follow' table, indicating that the current user follows the given user.
- If follow is false, the corresponding record is deleted from the 'follow' table.
- An 'ok' string is returned as the API response.

Set Add Status API:
- The `set_add_status` API updates the selected color in the session.
- The selected color is extracted from the JSON payload.
- The selected color is stored in the session for future reference.
- An 'ok' string is returned as the API response.

Comments Action:
- The `comments` action renders the 'comments.html' template for displaying comments related to a specific post.
- The post ID is extracted from the URL parameters and passed to the view template.

Mark Contact API:
- The `mark_contact` API updates the 'mark' field of a contact record in the database.
- The contact ID and mark value are extracted from the JSON payload.
- The contact record is retrieved from the database using the contact ID.
- If the contact exists, the 'mark' field is updated with the provided mark value.
- All contact IDs that are marked as True are printed (for debugging purposes).
- An 'ok' string is returned as the API response.

4. Conclusion:
This document has provided an overview and detailed description of the implementation of a web application with various actions and APIs. The implementation follows the MVC architecture and utilizes the web framework for rendering views and handling user requests. The actions and APIs enable functionalities such as managing posts, contacts, comments, user interactions, and more.
