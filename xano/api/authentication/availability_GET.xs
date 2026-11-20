query "availability" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int barber_id
    int service_id
    text date filters=trim
  }

  stack {
    db.get "user" {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "role", "active"]
    } as $actor

    precondition ($actor != null && $actor.active == true && $actor.role == "client") {
      error_type = "accessdenied"
      error = "Apenas clientes ativos podem consultar horários."
    }

    db.get "barber" {
      field_name = "id"
      field_value = $input.barber_id
    } as $barber

    precondition ($barber != null && $barber.active == true) {
      error_type = "inputerror"
      error = "Selecione um serviço e barbeiro ativos."
    }

    db.get "user" {
      field_name = "id"
      field_value = $barber.user_id
      output = ["id", "role", "active"]
    } as $barber_user

    db.get "service" {
      field_name = "id"
      field_value = $input.service_id
    } as $service

    precondition ($barber_user != null && $barber_user.active == true && $barber_user.role == "barber" && $service != null && $service.active == true && $service.duration_minutes != null && $service.duration_minutes > 0) {
      error_type = "inputerror"
      error = "Selecione um serviço e barbeiro ativos."
    }

    var $day_start_text {
      value = $input.date ~ " 00:00:00"
    }

    var $opening_text {
      value = $input.date ~ " 09:00:00"
    }

    var $closing_text {
      value = $input.date ~ " 18:00:00"
    }

    var $day_start {
      value = $day_start_text|parse_timestamp:"Y-m-d H:i:s":"America/Sao_Paulo"
    }

    var $opening {
      value = $opening_text|parse_timestamp:"Y-m-d H:i:s":"America/Sao_Paulo"
    }

    var $closing {
      value = $closing_text|parse_timestamp:"Y-m-d H:i:s":"America/Sao_Paulo"
    }

    var $day_end {
      value = $day_start|add_secs_to_timestamp:86400
    }

    var $weekday {
      value = $day_start|format_timestamp:"N":"America/Sao_Paulo"
    }

    var $earliest {
      value = now|add_secs_to_timestamp:7200
    }

    var $latest {
      value = now|add_secs_to_timestamp:2592000
    }

    var $candidate {
      value = $opening
    }

    conditional {
      if ($earliest > $opening) {
        var $earliest_minute_text {
          value = $earliest|format_timestamp:"Y-m-d H:i":"America/Sao_Paulo"
        }

        var $earliest_minute {
          value = $earliest_minute_text|parse_timestamp:"Y-m-d H:i":"America/Sao_Paulo"
        }

        var $earliest_seconds {
          value = $earliest|format_timestamp:"s":"America/Sao_Paulo"
        }

        conditional {
          if ($earliest_seconds == "00") {
            var.update $candidate {
              value = $earliest_minute
            }
          }

          else {
            var.update $candidate {
              value = $earliest_minute|add_secs_to_timestamp:60
            }
          }
        }
      }
    }

    db.query "appointment" {
      where = $db.appointment.barber_id == $input.barber_id && $db.appointment.start_time < $day_end && $db.appointment.end_time > $day_start && $db.appointment.status != "cancelled"
      output = ["start_time", "end_time"]
      return = {type: "list"}
    } as $busy

    var $slots {
      value = []
    }

    foreach (0|range:0:100) {
      each as $attempt {
        var $candidate_busy_end {
          value = $candidate|add_secs_to_timestamp:(($service.duration_minutes * 60) + 900)
        }

        conditional {
          if ($candidate_busy_end <= $closing && $candidate >= $earliest && $candidate <= $latest && $weekday != "7") {
            var $is_available {
              value = true
            }

            var $next_candidate {
              value = $candidate
            }

            foreach ($busy) {
              each as $existing {
                var $busy_end {
                  value = $existing.end_time|add_secs_to_timestamp:900
                }

                conditional {
                  if ($candidate < $busy_end && $candidate_busy_end > $existing.start_time) {
                    var.update $is_available {
                      value = false
                    }

                    conditional {
                      if ($busy_end > $next_candidate) {
                        var.update $next_candidate {
                          value = $busy_end
                        }
                      }
                    }
                  }
                }
              }
            }

            conditional {
              if ($is_available) {
                var.update $slots {
                  value = $slots|append:($candidate|format_timestamp:"H:i":"America/Sao_Paulo")
                }

                var.update $candidate {
                  value = $candidate|add_secs_to_timestamp:(($service.duration_minutes * 60) + 900)
                }
              }

              else {
                var.update $candidate {
                  value = $next_candidate
                }
              }
            }
          }
        }
      }
    }
  }

  response = {items: $slots}
  guid = "jQWyPpa3WWzRlxnwa1zCprJgvc4"
}
