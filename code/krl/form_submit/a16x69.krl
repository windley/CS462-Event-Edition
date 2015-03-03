ruleset a16x69 {
  meta {
    name "hello_world_with_name (Ch 7)"
    description <<
      
    >>
    author "Phil Windley"
    logging on
  }

  dispatch {
     // domain "byu.edu"
     // domain "foobar.com"
  }

  global {
  
  }

  rule clear_name is active {
     select when web pageview name re/clear/ 
     noop();
     always {
	clear ent:name;
	last
     }
   }

  rule initialize is active {
    select when pageview ".*"
     pre {   
      blank_div = <<
<div id="my_div">
</div>
      >>;
    }
    notify("Hello Example", blank_div)
	with sticky=true;
  }

  rule set_form is active {
    select when pageview ".*"
    pre {   
      a_form = <<
<form id="my_form" onsubmit="return false">
<input type="text" name="first"/>
<input type="text" name="last"/>
<input type="submit" value="Submit" />
</form>
      >>;
    }
    if(not seen ".*" in ent:name)  then {
      append("#my_div", a_form);
      watch("#my_form", "submit");
    }
    fired {
       last;
    }
  }

  rule respond_submit is active {
    select when web submit "#my_form"
    pre {
       first = page:param("first");
       last = page:param("last");

    }
    noop();
    fired {
       mark ent:name with first + " " + last;
       raise explicit event got_name
    }

  } 

  rule replace_with_name is active {
     select when explicit got_name 
	      or web pageview ".*" 
     pre {
       name = current ent:name;
     }
     replace_inner("#my_div", "Hello #{name}");
  }




}