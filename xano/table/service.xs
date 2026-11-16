table "service" {
  auth = false
  schema {
    int id
    text title filters=trim
    text description?
    decimal price filters=min:0.01
    int duration_minutes filters=min:1
    bool active?=true
    timestamp created_at?=now
    timestamp updated_at?=now
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "active"}]}
  ]
}
