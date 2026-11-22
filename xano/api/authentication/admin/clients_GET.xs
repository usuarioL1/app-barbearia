query "admin/clients" verb=GET {
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
      error = "Apenas administradores ativos podem consultar clientes."
    }

    db.query "user" {
      where = $db.user.role == "client"
      sort = {created_at: "desc"}
      output = ["id", "name", "email", "phone", "role", "active"]
      return = {type: "list"}
    } as $clients
  }

  response = {items: $clients}
}
