query "appointments/{id}/cancel" verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    int id
  }

  stack {
    db.get "user" {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "role", "active"]
    } as $actor

    precondition ($actor != null && $actor.active == true && ($actor.role == "client" || $actor.role == "admin")) {
      error_type = "accessdenied"
      error = "Seu perfil não pode cancelar este agendamento."
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

        precondition ($actor.role == "admin" || $appointment.client_id == $actor.id) {
          error_type = "accessdenied"
          error = "Você não tem acesso a este agendamento."
        }

        precondition ($appointment.status == "pending" || $appointment.status == "confirmed") {
          error_type = "inputerror"
          error = "Somente agendamentos pendentes ou confirmados podem ser cancelados."
        }

        conditional {
          if ($actor.role == "client") {
            var $cancellation_deadline {
              value = now|add_secs_to_timestamp:43200
            }

            precondition ($appointment.start_time >= $cancellation_deadline) {
              error_type = "inputerror"
              error = "O cancelamento deve ser feito com pelo menos 12 horas de antecedência."
            }
          }
        }

        db.edit "appointment" {
          field_name = "id"
          field_value = $appointment.id
          data = {
            status      : "cancelled"
            cancelled_at: now
            cancelled_by: $actor.id
            updated_at  : now
          }
        } as $updated

        db.add "appointment_status_history" {
          data = {
            appointment_id: $appointment.id
            from_status   : $appointment.status
            to_status     : "cancelled"
            changed_by    : $actor.id
            changed_at    : now
            notes         : "Agendamento cancelado"
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
  guid = "H44_zPwCPTDfx22iBgociVeTj-w"
}
