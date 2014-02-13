ruleset a16x66 {
  meta {
    name "echo"
    description <<
      Playing with an echo endpoint
    >>
    author "Phil Windley"
    logging on
  }

  rule hello_world is active {
    select when echo hello
    send_directive("say") with
      something = "Hello World";
  }
  
  rule echo is active {
    select when echo message input re#(.*)# setting(m)
    send_directive("say") with
      something = m;
  }
}