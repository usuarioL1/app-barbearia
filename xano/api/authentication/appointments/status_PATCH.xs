query "appointments/{id}/status" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int id
    enum status {
      values = ["pending", "confirmed", "cancelled", "completed"]
    }
  }

  stack {
    db.get "user" {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "role", "active"]
    } as $actor

    precondition ($actor != null && $actor.active == true && ($actor.role == "barber" || $actor.role == "admin")) {
      error_type = "accessdenied"
      error = "Somente o barbeiro responsável ou um administrador podem alterar o status."
    }

    var $barber_id {
      value = 0
    }

    conditional {
      if ($actor.role == "barber") {
        db.get "barber" {
          field_name = "user_id"
          field_value = $actor.id
        } as $barber

        precondition ($barber != null && $barber.active == true) {
          error_type = "accessdenied"
          error = "Perfil de barbeiro inativo."
        }

        var.update $barber_id {
          value = $barber.id
        }
      }
    }

    db.transaction {
      stack {
        db.get "appointment" {
          field_name = "id"
          field_value = $input.id
        } as $appointment

        precondition ($appointment != null) {
          error_type = "notfound"
          error = "Agendamento não encontrado."
        }

        precondition ($actor.role == "admin" || $appointment.barber_id == $barber_id) {
          error_type = "accessdenied"
          error = "Você não tem acesso a este agendamento."
        }

        var $transition_allowed {
          value = ($appointment.status == "pending" && ($input.status == "confirmed" || $input.status == "cancelled")) || ($appointment.status == "confirmed" && ($input.status == "completed" || $input.status == "cancelled"))
        }

        precondition ($transition_allowed == true) {
          error_type = "inputerror"
          error = "A transição de status solicitada não é permitida."
        }

        conditional {
          if ($input.status == "completed") {
            precondition ($appointment.end_time <= now) {
              error_type = "inputerror"
              error = "O atendimento só pode ser concluído após o horário de término."
            }
          }
        }

        var $update_data {
          value = {
            status    : $input.status
            updated_at: now
          }
        }

        conditional {
          if ($input.status == "cancelled") {
            var.update $update_data {
              value = $update_data|set:"cancelled_at":now|set:"cancelled_by":$actor.id
            }
          }
        }

        db.patch "appointment" {
          field_name = "id"
          field_value = $appointment.id
          data = $update_data
        } as $updated

        db.add "appointment_status_history" {
          data = {
            appointment_id: $appointment.id
            from_status   : $appointment.status
            to_status     : $input.status
            changed_by    : $actor.id
            changed_at    : now
            notes         : "Status atualizado"
          }
        } as $history
      }
    }
  }

  response = {
    id                       : $updated.id
    client_id                : $updated.client_id
    barber_id                : $updated.barber_id
    service_id               : $updated.service_id
    service_title_snapshot   : $updated.service_title_snapshot
    price_snapshot           : $updated.price_snapshot
    duration_minutes_snapshot: $updated.duration_minutes_snapshot
    start_time               : $updated.start_time|format_timestamp:"Y-m-d\\TH:i:sP":"America/Sao_Paulo"
    end_time                 : $updated.end_time|format_timestamp:"Y-m-d\\TH:i:sP":"America/Sao_Paulo"
    status                   : $updated.status
  }
  guid = "LG_jVEkRggxTlQygc8cMQ-K7u_8"
}
