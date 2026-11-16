query "auth/me" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    text name filters=trim
    email email filters=trim|lower
    text phone filters=trim
  }

  stack {
    precondition (($input.name|strlen) > 0 && ($input.phone|strlen) >= 10) {
      error_type = "inputerror"
      error = "Informe nome e telefone válidos."
    }

    db.get "user" {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "active"]
    } as $user

    precondition ($user != null && $user.active == true) {
      error_type = "unauthorized"
      error = "Sessão inválida ou expirada."
    }

    db.get "user" {
      field_name = "email"
      field_value = $input.email
      output = ["id"]
    } as $email_owner

    precondition ($email_owner == null || $email_owner.id == $auth.id) {
      error_type = "accessdenied"
      error = "Este e-mail já está em uso."
    }

    db.edit "user" {
      field_name = "id"
      field_value = $auth.id
      data = {
        name : $input.name
        email: $input.email
        phone: $input.phone
      }
    } as $updated_user

    function.run "Quick Start/log_event" {
      input = {user_id: $auth.id, action: "profile_updated"}
    } as $event_log
  }

  response = {
    id   : $updated_user.id
    name : $updated_user.name
    email: $updated_user.email
    phone: $updated_user.phone
    role : $updated_user.role
  }
}
