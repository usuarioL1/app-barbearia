table event_log {
  auth = false
  schema {
    int id
    int user_id? {
      table = "user"
    }
    text action filters=trim
    timestamp created_at?=now
    json metadata?
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id"}]}
  ]
  guid = "RRP0jAwiB0e-oPU4K6F_hqpTJuU"
}
