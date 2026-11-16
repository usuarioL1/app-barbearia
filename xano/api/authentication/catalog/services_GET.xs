query "services" verb=GET {
  api_group = "Authentication"

  input {
  }

  stack {
    db.query "service" {
      where = $db.service.active == true
      sort = {title: "asc"}
      return = {type: "list"}
    } as $services
  }

  response = {items: $services}
}
