// Pull all event logs for the authenticated user
query "logs/user/my_events" verb=GET {
  api_group = "Event Logs"
  auth = ""

  input {
  }

  stack {
    // Retrieve event logs for the authenticated user
    db.query "" {
      where = $db.event_log.user_id == $auth.id
      output = ["id", "created_at", "user_id", "action"]
      return = {type: "list"}
    } as $user_events
  }

  response = $user_events
  tags = ["xano:quick-start"]
  guid = "Im6Ie4paFgBZEv8J6sIF-sg6m0o"
}