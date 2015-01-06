ruleset a16x171 {
  meta {
    name "Hello World"
    description <<
      Hello World
    >>
    author ""
    // Uncomment this line to require Marketplace purchase to use this app.
    // authz require user
    logging on
  }

  dispatch {
    // Some example dispatch domains
    // domain "example.com"
    // domain "other.example.com"
  }

  global {
  
  }

  rule test_rule is active {
    select when pageview ".*" setting ()
    // pre {   }
    notify("Hello World", "This is a sample rule for cs462.") with
      sticky = true;
  }


}