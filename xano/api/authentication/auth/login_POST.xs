// Login and retrieve an authentication token
query "auth/login" verb=POST {
  api_group = "Authentication"

  input {
    email email filters=trim|lower
    text password
  }

  stack {
    // Get the user record via email
    db.get "user" {
      field_name = "email"
      field_value = $input.email
      output = ["id", "created_at", "name", "email", "password", "phone", "role", "active"]
    } as $user
  
    // Check to make sure a user with that email exists
    precondition ($user != null) {
      error_type = "unauthorized"
      error = "E-mail ou senha inválidos."
    }

    precondition ($user.active == true) {
      error_type = "unauthorized"
      error = "E-mail ou senha inválidos."
    }
  
    // Check that the password matches the hashed password
    security.check_password {
      text_password = $input.password
      hash_password = $user.password
    } as $pass_result
  
    // Verify that the password check passed
    precondition ($pass_result) {
      error_type = "unauthorized"
      error = "E-mail ou senha inválidos."
    }

    db.get "account_security" {
      field_name = "user_id"
      field_value = $user.id
    } as $security

    var $session_version {
      value = $security != null ? $security.session_version : 0
    }
  
    // Create an authentication token
    security.create_auth_token {
      table = "user"
      extras = {session_version: $session_version}
      expiration = 86400
      id = $user.id
    } as $authToken
  
    // Create an event log for login
    function.run "Quick Start/log_event" {
      input = {user_id: $user.id, action: "login"}
    } as $event_log
  }

  response = {
    authToken: $authToken
    user: {
      id   : $user.id
      name : $user.name
      email: $user.email
      phone: $user.phone
      role : $user.role
    }
  }
  tags = ["xano:quick-start"]
  guid = "Nwekz8KkBWX1HEiIzdbqMsECLvQ"
}