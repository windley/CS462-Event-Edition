ruleset a16x166 {
  meta {
    name "Light Controller"
    description <<
An app for interacting with the Hue service to control Hue lights.
>>
    author "Phil Windley"
    logging on
    use module a16x165 alias hue
    use module a169x676 alias pds
    use module a169x701 alias CloudRain
    use module a169x664 alias CloudUI

   // use javascript resource "https://raw.github.com/DavidDurman/FlexiColorPicker/master/colorpicker.min.js"

  }

  dispatch {
  }

  global {

    myDivID ="hue-#{meta:rid()}";
    myDivIDSelector ="##{myDivID}";
    initial_fields = <<
<div style="margin: 20px" id="#{myDivID}" ></div>
<div id="alertForgot" class="alert alert-info" style="display:none;"></div>
<div style="margin: 20px">
<form class="form-horizontal" id="formHue">
  <fieldset>
   <h4>Hue Lights</h4>
   <div class="control-group"> 
    <label class="control-label" for="bulb">Light</label>
    <div class="controls">
    <label class="radio inline">
      <input type="radio" name="bulb" value="1"> 1
    </label>
    <label class="radio inline">
      <input type="radio" name="bulb"  value="2"> 2
    </label>
    <label class="radio inline">
      <input type="radio" name="bulb"  value="3"> 3
    </label>
    <label class="radio inline">
      <input type="radio" name="bulb"  value="4"> 4
    </label>
    </div>
   </div>

   <div class="control-group">
    <label class="control-label" for="hue">Hue (0..360)</label>
    <div class="controls">
      <input class="input-mini" type="text" name="hue" id="hue" placeholder="0">
    </div>
  </div>

  <div class="control-group">
    <label class="control-label" for="sat">Saturation (0..1)</label>
    <div class="controls">
      <input class="input-mini" type="text" name="sat" id="sat" value="1.0">
    </div>
  </div>

  <div class="control-group">
    <label class="control-label" for="li">Lightness (0..1)</label>
    <div class="controls">
      <input class="input-mini" type="text" name="li" id="li" value="0.5">
    </div>
  </div>
  <div class="control-group">
    <div class="controls">
      <button type="submit" class="btn btn-primary">Go</button>
    </div>
  </div>
  <div class="control-group">
   <h4>All Lights</h4>
    <div class="controls"> 
     <a href="#!/app/#{meta:rid()}/all_on" class="btn btn-success">All On</a>
     <a href="#!/app/#{meta:rid()}/all_off" class="btn btn-danger">All Off</a> 
    </div>
  </div>
 </fieldset>
</form>
</div>
>>;
  }



  rule turn_one_on {
    select when office door_open
     // {
     //  hue:all_on_in_group(0);
     // }
    always {
      raise explicit event office_lights
        with state = "on"
    }
  }

  rule turn_one_off {
    select when office door_closed
     // {
     //  hue:all_off_in_group(0);
     // }
    always {
      raise explicit event office_lights
        with state = "off"
    }
  }



  rule set_temp_color {
    select when thermostat temperature
    pre {
      trend =  pds:get_item('thermostat','last_temp_trend');
       // hue = trend eq 'red'   => 3000 |
       //       trend eq 'green' => 40000 |
       //                           15000;

      hue = trend eq 'red'   => 8 |
            trend eq 'green' => 240 |
                                55;

    }
    hue:set_bulb_hsl(1, hue, 1.0, 0.50);
  }


  // ------------------------------------------------------------------------
  // for dashboard interaction
  // ------------------------------------------------------------------------
  rule appHue_Selected {
    select when web cloudAppSelected
	   or   web cloudAppAction
    pre {
      appMenu = [];
    }
    CloudRain:createPanel("Light Controller", appMenu);
  }

  // ------------------------------------------------------------------------
  rule appHue_Created {
    select when web cloudAppSelected
	   or   web cloudAppAction action re/first/
    pre {
      appContent = <<
#{initial_fields}
>>;
    }
    {
      CloudRain:loadPanel(appContent);
      CloudRain:skyWatchSubmit("#formHue", "");
    }
  }

  rule appHue_allOn {
    select when web cloudAppAction action re/all_on/
    pre {
      appContent = <<
Light are all on.
>>;
    }
    {
      CloudUI:showAlert("#alertForgot", appContent);
      CloudRain:hideSpinner();
    }
    always {
      raise explicit event office_lights
        with state = "on"
    }

  }
  
  rule appHue_allOff {
    select when web cloudAppAction action re/all_off/
    pre {
      appContent = <<
Lights are all off.
>>;
    }
    {
      CloudUI:showAlert("#alertForgot", appContent);
      CloudRain:hideSpinner();
    }
    always {
      raise explicit event office_lights
        with state = "off"
    }

  }
  

  rule appHue_form_submit {
    select when web submit "#formHue"
    pre {
  //      action = event:attrs().encode();
 //       appContent = <<
 // Attrs: #{action}
 // >>;
      appContent = <<
Updated bulb #{event:attr("bulb")} with HSL=(#{event:attr("hue")}, #{event:attr("sat")}, #{event:attr("li")}) 
>>;
    }
    {
//      replace_inner(myDivIDSelector, appContent);
      CloudRain:hideSpinner();
      CloudUI:showAlert("#alertForgot", appContent);
      hue:set_bulb_hsl(event:attr("bulb"), event:attr("hue"), event:attr("sat"), event:attr("li") );
    }
  }


}