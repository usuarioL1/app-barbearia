// Signup and retrieve an authentication token
query "auth/signup" verb=POST {
  api_group = "Authentication"

  input {
    text name filters=trim
    email email filters=trim|lower
    text phone filters=trim
    text password
  }

  stack {
    precondition (($input.name|strlen) > 0) {
      error_type = "inputerror"
      error = "Informe seu nome."
    }

    precondition (($input.phone|strlen) >= 10) {
      error_type = "inputerror"
      error = "Informe um telefone válido."
    }

    precondition (($input.password|strlen) >= 8) {
      error_type = "inputerror"
      error = "A senha deve conter pelo menos 8 caracteres."
    }

    // Check if a user record with that email exists
    db.get "" {
      field_name = "email"
      field_value = $input.email
    } as $user
  
    // Verify that the email being used to sign up is unique
    precondition ($user == null) {
      error_type = "accessdenied"
      error = "An account with this email already exists."
    }
  
    // Create a new user record
    db.add "" {
      data = {
        created_at: "now"
        name      : $input.name
        email     : $input.email
        password  : $input.password
        phone     : $input.phone
        role      : "client"
        active    : true
      }
    } as $user
  
    // Create an authentiction token
    security.create_auth_token {
      table = ""
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken
  
    // Create an event log for signup
    function.run "Quick Start/log_event" {
      input = {user_id: $user.id, action: "signup"}
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
  guid = "QWzo6DXCZ27TK81Sbkb3O5ADW8w"
}