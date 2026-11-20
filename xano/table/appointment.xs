table "appointment" {
  auth = false
  schema {
    int id
    int client_id {
      table = "user"
    }
    int barber_id {
      table = "barber"
    }
    int service_id {
      table = "service"
    }
    text service_title_snapshot filters=trim
    decimal price_snapshot filters=min:0
    int duration_minutes_snapshot filters=min:1
    timestamp start_time
    timestamp end_time
    enum status?="pending" {
      values = ["pending", "confirmed", "cancelled", "completed"]
    }
    timestamp created_at?=now
    timestamp cancelled_at?
    int cancelled_by? {
      table = "user"
    }
    timestamp updated_at?=now
    text notes?
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "client_id"}, {name: "start_time", op: "desc"}]}
    {type: "btree", field: [{name: "barber_id"}, {name: "start_time"}]}
    {type: "btree", field: [{name: "status"}, {name: "start_time"}]}
  ]
  guid = "VvPUMPegSEjpt6yi0Vb_F0nsIts"
}
