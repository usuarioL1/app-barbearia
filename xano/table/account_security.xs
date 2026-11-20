table "account_security" {
  auth = false
  schema {
    int id
    int user_id {
      table = "user"
    }
    text avatar_url?
    int session_version?=0
    bool totp_enabled?=false
    text totp_secret?
    text pending_totp_secret?
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "user_id"}]}
  ]
  guid = "aLbF4N7GeScPfVqj_cG6lOZLF6M"
}
