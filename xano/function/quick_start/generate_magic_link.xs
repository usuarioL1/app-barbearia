function "Quick Start/generate_magic_link" {
  input {
    email email filters=trim|lower
  }

  stack {
    db.get "user" {
      field_name = "email"
      field_value = $input.email
      output = ["id", "email", "active"]
    } as $user

    var $reset_link {
      value = {token: "", email: $input.email}
    }

    conditional {
      if ($user != null && $user.active == true) {
        security.create_uuid as $token

        db.add_or_edit "password_reset" {
          field_name = "user_id"
          field_value = $user.id
          data = {
            user_id   : $user.id
            token_hash: $token
            expires_at: now|add_secs_to_timestamp:3600
            used      : false
          }
        } as $reset_record

        var.update $reset_link {
          value = $reset_link|set:"token":$token
        }
      }
    }
  }

  response = $reset_link
  tags = ["barberflow:auth"]
}
