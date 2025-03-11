# ProDev-SocialMediaFeedAPI

Welcome to **ProDev-SocialMediaFeedAPI**! This API allows developers to create, manage, and interact with social media posts using GraphQL. Whether you're building a social media application, a blog, or a community platform, this API provides essential features to facilitate user engagement through posts and comments.

## Features

- **User Authentication**: Create and log in users with JWT authentication.
- **Create Posts**: Easily create new posts with text, images, and other media.
- **Commenting System**: Users can comment on posts, fostering interaction and discussion.
- **Like and Dislike**: Users can express their opinions by liking or disliking posts and comments.
- **Flexible Queries**: Use GraphQL to fetch posts, comments, and user interactions with precise control over the data you need.

## Getting Started

Follow these steps to set up and run the API:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ProDev-SocialMediaFeedAPI.git
cd ProDev-SocialMediaFeedAPI
```

### 2. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the root directory and add your database connection settings and any other configuration variables. By default it will use sqlite3 database

### 4. Run the API

```bash
python3 manage.py runserver
```

### 5. Access GraphQL Playground

Open your browser and navigate to `http://localhost:8000/graphql` to access the GraphQL Playground, where you can test queries and mutations.

---

## User Authentication

### Create a User

```graphql
mutation {
  UserCreate(username: "newuser", firstName: "First", lastName: "Last", email: "user@example.com", password: "password123") {
    success
    error
    user {
      id
      username
      email
    }
  }
}
```

### Login a User

```graphql
mutation {
  UserToken(username: "newuser", password: "password123") {
    success
    error
    token
    user {
      id
      username
      email
    }
  }
}
```

### Authorization Header

When making requests that require authentication, include the JWT token in the `Authorization` header:

```
Authorization: jwt <token_here>
```

---

## Queries

### Get Logged-in User

```graphql
query {
  loggedUser {
    id
    username
    email
  }
}
```

### Get All Posts

```graphql
query {
  allPosts(first: 10, titleContains: "First") {
    id
    title
    content
    interactionsCount
  }
}
```

### Get a Specific Post

```graphql
query {
  post(id: 1) {
    id
    title
    content
    interactionsCount
  }
}
```

### Get Comments for a Post

```graphql
query {
  commentsForPost(postId: 1) {
    id
    content
    user {
      username
    }
  }
}
```

### Get Interactions

```graphql
query {
  interactions(username: "newuser", postId: 1) {
    id
    interactionType
  }
}
```
---

## Mutations

### Create a Post

```graphql
mutation {
  PostCreate(title: "My First Post", content: "This is the content of my first post!") {
    success
    error
    post {
      id
      title
      content
    }
  }
}
```

### Update a Post

```graphql
mutation {
  PostUpdate(postId: 1, title: "Updated Title", content: "Updated content.") {
    success
    error
    post {
      id
      title
      content
    }
  }
}
```

### Delete a Post

```graphql
mutation {
  PostDelete(postId: 1) {
    success
    error
  }
}
```
---

## Conclusion

The **ProDev-SocialMediaFeedAPI** provides a robust and flexible solution for managing social media interactions with GraphQL. With authentication, post creation, comments and likes, it is an excellent foundation for social media applications. Happy coding! 🚀


