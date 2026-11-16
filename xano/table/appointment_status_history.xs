table "appointment_status_history" {
  auth = false
  schema {
    int id
    int appointment_id {
      table = "appointment"
    }
    enum from_status? {
      values = ["pending", "confirmed", "cancelled", "completed"]
    }
    enum to_status {
      values = ["pending", "confirmed", "cancelled", "completed"]
    }
    int changed_by {
      table = "user"
    }
    timestamp changed_at?=now
    text notes?
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "appointment_id"}, {name: "changed_at"}]}
  ]
}
