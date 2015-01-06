ruleset a16x149 {
	meta {
	  name "CT30 Thermostat Service"
	  description <<
Interacts with Radio Thermostat CT-30
		>>
  	  author "Phil Windley"
	  logging on
        
          key cosm {"api_key": "ACa7J_vfnpoxtGPT-mWe5Xa9VslR92NRRW4OgVJMapE"}
         
          use module a16x150 version "dev" alias cosm with
            api_key = keys:cosm("api_key") and
            feed_id = "66017"

          use module a16x153 version "dev" alias radstat

          use module a8x114 alias gcal with
            url = "https://www.google.com/calendar/feeds/mf4ob4114t0f4sgjjhdmmirfjc%40group.calendar.google.com/public/basic"
	}

	dispatch {
	  //domain "exampley.com"
//	  domain "byu.edu"
	  //domain "windley.com"
	}

	global {
	  lower_threshold = 60;
	  upper_threshold = 120;
          bound = 1; // anti-bounce value
	  within_bound = function(x, y, bound) {
	    x >= y-bound && x <= y + bound
	  };

       }

	rule set_avg_temperature {
          select when repeat 5 (thermostat temperature temperature "(.*)") avg(avg_temp)
          always {
            set ent:avg_temp avg_temp;
          }
        }

	rule set_trend_light {
	  select when thermostat temperature
	  pre {
            temperature = event:attr("temperature");
            color = within_bound(temperature, ent:avg_temp, 0.2) => "yellow" |
 	     	    (temperature < ent:avg_temp)                 => "green"    |
                    (temperature > ent:avg_temp)                 => "red"  | 
		    	                                            "off"    
	  }
	  radstat:set_color(color);
          fired {
            set ent:last_temp_trend color;
          }
        }		      

	rule get_temperature_target {
          select when thermostat temperature
          pre {
            event_detail = gcal:now("/Temperature/");
            target_temps = event_detail.pick("$..title").extract(re/(\d\d)\s*-\s*(\d\d)/);
            max_temp = target_temps.length() == 2 && target_temps[1];
            min_temp = target_temps.length() == 2 && target_temps[0];
          }
	  if(max_temp && min_temp) then noop();
          fired {
            set ent:max_temp_target max_temp;
            set ent:min_temp_target min_temp;
  	    raise explicit event new_target_temperature 
              with max_temp = max_temp
               and min_temp = min_temp;
            log "Target temperature: #{min_temp} - #{max_temp}";
          }
        }

	// reset if someone plays with thermostat
	rule reset_target_and_mode {
	  select when thermostat temperature
	  pre {
	    thermostat_mode = event:attr("mode") || ent:curr_mode;
	    thermostat_target = event:attr("target") || ent:curr_target;
	  }
          if(ent:curr_mode neq thermostat_mode ||            
	     ent:curr_target neq thermostat_target
  	    ) then radstat:set_temperature(ent:curr_mode, ent:curr_target);
	  fired {
	    raise explicit event updated_thermostat
              with mode = ent:curr_mode
               and target_temp = ent:curr_target;
	  }
	}

	rule set_target_and_mode {
	  select when explicit new_target_temperature
	  pre {
            curr_temperature = event:attr("temperature");
	    max_temp = event:attr("max_temp") || ent:max_temp_target;
	    min_temp = event:attr("min_temp") || ent:min_temp_target;
	    mode = (curr_temperature > max_temp+bound) => "cool" |
	           (curr_temperature < min_temp-bound) => "heat" |
							  "no_change";
            temperature = (mode eq "cool") => max_temp |
                          (mode eq "heat") => min_temp |
                                              curr_temperature;
	  }
          if(mode neq ent:curr_mode || 
	     temperature neq ent:curr_target 
  	    ) then { 
  	    radstat:set_temperature(mode, temperature);
          }
          fired {
            set ent:curr_mode mode; // current mode of thermostat
            set ent:curr_target temperature; // current target temperature
  	    raise explicit event updated_thermostat
              with mode = mode
               and target_temp = temperature;
            log "Setting mode to #{mode} for temperature #{temperature}"
          }
        }		      

	rule process_temperature {
	  select when thermostat temperature
          pre {
            temperature = event:attr("temperature");
             // new_array = (ent:temps.length() == 5) => ent:temps.tail().append(temperature) |
             //             (ent:temps.length() == 0) => [temperature] |
             //                                          ent:temps.append(temperature);
             // avg_temp = average(new_array);
	     
          }
          if (temperature >= lower_threshold && temperature <= upper_threshold) then {
            cosm:update("Temperature", temperature);
            cosm:update("AvgTemperature", ent:avg_temp);
            cosm:update("MaxTargetTemp", ent:max_temp_target);
            cosm:update("MinTargetTemp", ent:min_temp_target);
          }
          fired {
            set ent:last_temp temperature;
            set ent:last_temp_time time:now();
            set ent:temps new_array;
          }
	}

    rule save_temp_values {
      select when thermostat temperature
      always {
        raise pds event new_map_available with
          namespace = 'thermostat' and
          mapvalues = {'last_temp_time' : ent:last_temp_time,
                       'last_temp' : ent:last_temp,
                       'last_temp_trend' : ent:last_temp_trend || 'unknown',
                       'avg_temp' : ent:avg_temp || 'unknown',
                       'min_temp_target' : ent:min_temp_target,
                       'max_temp_target' : ent:max_temp_target,
                       'curr_target' : ent:curr_target,
                       'curr_mode' : ent:curr_mode
          }
      }
    }

        rule show_temperature is inactive {
          select when web pageview 
      	  pre {
            msg = <<
#{ent:last_temp} degrees at #{time:strftime(ent:last_temp_time, '%c')}. <br/>
Trending #{ent:last_temp_trend || 'unknown'}. <br/>
We calculated #{ent:avg_temp || 'unknown'} from the compound eventex.<br/>
The current target temp range is #{ent:min_temp_target}-#{ent:max_temp_target} degrees.  </br/>
The thermostat is in #{ent:curr_mode} mode with a target temperature of #{ent:curr_target}.
                  >>;
          }
          notify("Most Recent Office Temperature", msg);
    	}
    
}
