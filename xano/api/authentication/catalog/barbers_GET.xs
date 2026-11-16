query "barbers" verb=GET {
  api_group = "Authentication"

  input {
  }

  stack {
    db.query "barber" {
      join = {
        user: {
          table: "user"
          type : "inner"
          where: $db.barber.user_id == $db.user.id
        }
      }
      eval = {
        name: $db.user.name
      }
      where = $db.barber.active == true && $db.user.active == true
      sort = {id: "asc"}
      return = {type: "list"}
    } as $barbers
  }

  response = {items: $barbers}
}
