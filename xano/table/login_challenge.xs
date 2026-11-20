table "login_challenge" {
  auth = false
  schema {
    int id
    int user_id {
      table = "user"
    }
    text challenge_id
    timestamp expires_at
    bool consumed?=false
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "challenge_id"}]}
  ]
  guid = "Yxb0iWzvHypjxFUQ5UVPFPlXiyU"
}
