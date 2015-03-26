ruleset test_eventnames {

  rule foo {
    select when songs reset
    noop();
  }

}