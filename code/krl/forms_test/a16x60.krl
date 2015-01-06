ruleset a16x60 {
meta {
  name "Forms Test"
  description << 
Testing forms in KRL
  >>
  author "Phil Windley"
  logging on
}

dispatch {
  domain "byu.edu"
}

global { 
}

rule set_form is active {
  select when pageview ".*" setting ()
  pre {   
    a_form = <<
<div id="my_div">
<form id="my_form" onsubmit="return false">
<input type="text" name="first"/>
<input type="text" name="last"/>
<input type="submit" value="Submit" />
</form>
<ul id="mydata">
</ul>
</div>
    >>;
  // use this form to test if processing makes everything better
  my_form_new = <<
<div id="my_div">
<form id="my_form" action="javascript:function(){return false;}">
<input type="text" name="a" value="1" id="a" />
  <input type="text" name="b" value="2" id="b" />
  <input type="password" name="i" value="10" id="i" />
  <input type="hidden" name="c" value="3" id="c" />
  
    <textarea name="d" rows="8" cols="40">4</textarea>

<select name="e">
    <option value="5" selected="selected">5</option>
    <option value="6">6</option>
    <option value="7">7</option>
  </select>

    <input type="checkbox" name="f" value="8" id="f" />
    <input type="radio" name="g" value="9" id="g"/>

    <input type="submit" name="h" value="Submit" id="h" />
</form>
<ul id="mydata">
</ul>
</div>
    >>
  }
  {
  notify("Tell us your name...", a_form)
    with sticky=true;
  watch("#my_form", "submit");
  watch("#Breadcrumb", "click");
  watch("#edit-search-theme-form-keys", "change");
  watch(".dt", "click");
  
  }

}

rule logo_changed is active {
  select when web click ".dt"
  pre {
     text = "<br>I changed again from rule</br>";
  }
  append("#regular_logo", text);
}



rule respond_submit is active {
  select when web submit "#my_form"
  pre {
     first = page:param("first");
     last = page:param("last");
     text = "<li>Your name is #{first} #{last}</li>";
  }
  append("#mydata", text);

} 

rule respond_click is active {
  select when web click "#Breadcrumb"
  pre {
     text = "<li> Stop clicking me!!!!</li>";
  }
  append("#Breadcrumb", text);

}

rule respond_change is active {
  select when web change "#edit-search-theme-form-keys"
  pre {
     text = "Type something intelligible";
  }
  prepend("#userLogin", text);

}


}