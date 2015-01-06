ruleset a16x164 {
  meta {
    name "Temperature"
    description <<
Show the temperature from the PDS. 
    >>
    author "Phil Windley"
    logging on


    use module a169x701 alias CloudRain
     // use module a169x625 alias CloudOS
     // use module a169x664 alias cloudUI
    use module a169x676 alias pds
  }

  global {
    thisRID = meta:rid();

    get_config_value = function (name) {
      pds:get_setting_data_value(meta:rid(), name);
    };
    unit = get_config_value("unit");
    f_to_c = function(f) { (f +    -32) * 5 /9 };
    f_to_k = function(f) { f_to_c(f) + 273.15 };

    get_next_state = function () {
      set_threshold = function(name, value) {
        threshold = get_config_value(name);
        threshold eq "none" => value | threshold
      };
      upper = set_threshold('upper_threshold', 9999);
      lower = set_threshold('lower_threshold', -9999);
      results = event:attr("temperature") > upper => ["upper", upper] |
                event:attr("temperature") < lower => ["lower", lower] |
                                                     ["normal", 0];
      results
    }
  }

  // ------------------------------------------------------------------------
  rule appTemplate_Selected {
    select when web cloudAppSelected
           or   web cloudAppAction
    pre {
       appMenu = [];
    }
    CloudRain:createAppPanel(thisRID, "Temperature", appMenu);
  }

  // ------------------------------------------------------------------------
  rule appTemplate_Created {
    select when web cloudAppSelected
           or   web cloudAppAction action re/first/
    pre {
      appContentSelector = event:attr("appContentSelector");
      temperature_data = pds:get_items('thermostat');
      last_temp =  pds:get_item('thermostat','last_temp');
      show_temp = (unit eq "C") => f_to_c(last_temp) |
                  (unit eq "K") => f_to_k(last_temp) |
                                   last_temp;


      last_temp_time = temperature_data{'last_temp_time'};
      trend = temperature_data{'last_temp_trend'};
      
      trend_img = trend eq 'red'   => "warmer.png"    |
                  trend eq 'green' => "colder.png"    |
                                      "no_change.png" ;
      
      appContent = <<

<div style="height: 25px"></div>
<div style="margin-left:20px;margin-bottom:20px">
<span style="font-size: 108px">#{show_temp.sprintf("%.1f")}&deg;</span><span style="font-size: 96px">#{unit}</span> 
<img style="position:absolute; top:50%;" src="http://www.windley.com/images/#{trend_img}"/><br/>
<span style="font-size:10px;float:left">Recorded: #{time:strftime(last_temp_time, '%c')} GMT </span>
</div>

	>>;
    }
    CloudRain:loadAppPanel(thisRID, appContent);
  }

  rule threshold {
    select when thermostat temperature   
    pre {
      results = get_next_state();
      new_state = results[0];
      current_state = ent:threshold_state  || "normal";
      change_state = new_state neq current_state;
      msg = new_state neq "normal" => "The temperature has crossed the #{results[0]} threshold of #{results[1]}" 
                                    | "The temperature has returned to normal";
      sbj = new_state neq "normal" => "#{results[0].uc()} Threshold Crossed"
                                    | "Temperature Threshold Crossed";
    }
    // handle everything but a move from normal
    if change_state then
      send_directive("noop");
    fired {
      set ent:threshold_state new_state;
      raise notification event status with
        priority = 2 and	 
        application = meta:rulesetName() and
        subject = sbj and
        description = msg
    }
  }


  // ----------------------------------- configuration setup ---------------------------------------
  rule load_app_config_settings {
    select when web sessionLoaded
    pre {
      schema = [
        {
          "name"     : "unit",
          "label"    : "Temperature Unit",
          "dtype"    : "radio",
          "options"  : ["F","C","K"]
        },
        {
          "name"     : "lower_threshold",
          "label"    : "Lower Threshold",
          "dtype"    : "select",
          "options"  : ["none", "62", "63", "64", "65", "66", "67", "68", "69", "70"]
        },
        {
          "name"     : "upper_threshold",
          "label"    : "Upper Threshold",
          "dtype"    : "select",
          "options"  : ["none", "70", "71", "72", "73", "74", "75", "76", "77", "78"]
        }
      ];
      data = {
        "unit"  : "F",
	"lower_threshold" : "none",
	"upper_threshold" : "none"
      };
    }
    always {
      raise pds event new_settings_schema
        with setName   = meta:rulesetName()
        and  setRID    = thisRID
        and  setSchema = schema
        and  setData   = data
        and  _api = "sky";
    }
  }


}

