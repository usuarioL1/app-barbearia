query "admin/users" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.get "user" {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "role", "active"]
    } as $actor

    precondition ($actor != null && $actor.active == true && $actor.role == "admin") {
      error_type = "accessdenied"
      error = "Apenas administradores ativos podem consultar usuários."
    }

    db.query "user" {
      sort = {created_at: "desc"}
      output = ["id", "name", "email", "phone", "role", "active"]
      return = {type: "list"}
    } as $users
  }

  response = {items: $users}
}
