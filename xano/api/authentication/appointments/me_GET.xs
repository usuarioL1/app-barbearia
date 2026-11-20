query "appointments/me" verb=GET {
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

    precondition ($actor != null && $actor.active == true && $actor.role == "client") {
      error_type = "accessdenied"
      error = "Apenas clientes ativos podem consultar seus agendamentos."
    }

    db.query "appointment" {
      join = {
        barber: {table: "barber", where: $db.appointment.barber_id == $db.barber.id}
        barber_user: {table: "user", where: $db.barber.user_id == $db.barber_user.id}
      }
      where = $db.appointment.client_id == $actor.id
      sort = {start_time: "asc"}
      eval = {
        barber_name: $db.barber_user.name
      }
      output = ["id", "client_id", "barber_id", "service_id", "service_title_snapshot", "price_snapshot", "duration_minutes_snapshot", "start_time", "end_time", "status"]
      return = {type: "list"}
    } as $appointments

    var $items {
      value = []
    }

    foreach ($appointments) {
      each as $appointment {
        var $status {
          value = $appointment.status
        }

        conditional {
          if ($status == null) {
            var.update $status {
              value = "pending"
            }
          }
        }

        var $item {
          value = {
            id                       : $appointment.id
            client_id                : $appointment.client_id
            barber_id                : $appointment.barber_id
            barber_name              : $appointment.barber_name
            service_id               : $appointment.service_id
            service_title_snapshot   : $appointment.service_title_snapshot
            price_snapshot           : $appointment.price_snapshot
            duration_minutes_snapshot: $appointment.duration_minutes_snapshot
            start_time               : $appointment.start_time|format_timestamp:"Y-m-d\\TH:i:sP":"America/Sao_Paulo"
            end_time                 : $appointment.end_time|format_timestamp:"Y-m-d\\TH:i:sP":"America/Sao_Paulo"
            status                   : $status
          }
        }

        var.update $items {
          value = $items|push:$item
        }
      }
    }
  }

  response = {items: $items}
  guid = "i7-3zmk5OBQMnvB7SSKfaVQivYg"
}
