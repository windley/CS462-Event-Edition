
# Event Intermediaries


## Rule Chaining

- Isolate common functionality (DRY)
- Simplify rule interactions
- Permits rules to wait on intermediate actions

See form-submit example ([a16x69.krl](../code/krl/form_submit/a16x69.krl)). Also shows the following:

* initialize and populate rule pattern
* entity storage
* explicit events

## Logging

- Make records of actions without cluttering up the primary rule.

		rule finalize_new_users {
			select when fuse new_fleet_initialized
					and pds profile_updated
			pre {

	           me = pds:get_all_me();
		       my_email =  me{"myProfileEmail"} || random:uuid();
			   msg = <<
		         A new fleet was created for #{me.encode()} with ECI #{meta:eci()}
		       >>;
		   }

			{
				sendgrid:send("Kynetx Fleet Team", "pjw@kynetx.com", "New Fuse Fleet", msg);
			}

		    always {
		      set app:fuse_users{my_email} makeAcctRecord(me)
		    }
		}

## Abstract Events

- Add meaning to an event


		rule ignition_status_changed  {  
			select when carvoyant ignitionStatus
			pre {

			   status = event:attr("ignitionStatus");
			   tid = event:attr("tripId");
			   trip_data = event:attrs()
							 .put(["timestamp"], common:convertToUTC(time:now()))
						 .delete(["_generatedby"]);
			 }
			 noop();
			 always {
			   raise fuse event "new_trip" with tripId = tid if status eq "OFF";
			   raise fuse event "trip_check" with duration = 2 if status eq "ON"; 
			   raise fuse event "need_vehicle_status";
			   raise pds event "new_data_available"
					 attributes {
					   "namespace": namespace(),
					   "keyvalue": "ignitionStatus_fired",
					   "value": trip_data,
						   "_api": "sky"

					 };      
			 }
		   }


## Event Preprocessing

- Enrich the event


		  rule dtc_status_changed  { 
			select when carvoyant troubleCode
			pre {
			  codes = event:attr("troubleCodes");
			  id = event:attr("id");

			  details = dataSet(event:attr("vehicleId"),event:attr("dataSetId"));

			  detail = details
					     .filter(function(rec) {rec{"key"} eq "GEN_DTC"} ); 

			  reason_string = detail
						         .map( function(rec) { rec{"translatedValue"} } )
					             .join("; ");

			  status = event:attrs()
							  .put(["timestamp"], common:convertToUTC(time:now()))
							  .put(["translatedValues"], reason_string)
						      .delete(["_generatedby"]);
			}
			noop();
			always {
			  log "Recorded trouble codes: " + codes.encode();
			  raise pds event "new_data_available"
				  attributes {
					"namespace": namespace(),
					"keyvalue": "troubleCode_fired",
					"value": status,
						"_api": "sky"
  			       };
			   raise fuse event "updated_dtc"
				  with dtc = codes
				   and timestamp = status{"_timestamp"} 
				   and activity = "Vehicle reported the following diagnostic codes: #{codes.encode()}"
				   and reason = "Diagnostic code report from vehicle: #{reason_string}"
				   and id = id ;
			}
		  }

Where ```dataSet()``` is a function that makes a call out to an API and gets more data. 

		dataSet = function(vid, sid) {
		  config_data = get_config(vid).klog(">>> Config data in dataSet >>>>>");
		  dataset_url = config_data{"base_url"} + "/dataSet/#{sid}";
		  params = {};
		  result = carvoyant_get(dataset_url, config_data, params);
		  result{"status_code"} eq "200" => result{["content","dataSet", "datum"]}
										  | mk_error(result)
		}

## Event Stream Splitting

- Raise different events depending on the nature of the incoming event

		rule pinentered is active {
		  select when webhook pinentered
		  pre {
			pinattempt = event:param("Digits");
			phone = datasource:pds({"key":"phone"});
			pin = phone.pick("$..value.pin");
		  }
		  if pinattempt == pin then
			noop();
		  fired {
			raise explicit event correct_pin
		  } else {
			raise explicit event bad_pin
		  }
		}

## Error Processing

- Handle error conditions

		  rule carvoyant_http_fail {
			select when http post status_code re#([45]\d\d)# setting (status)
					 or http put status_code re#([45]\d\d)# setting (status)
					 or http delete status_code re#([45]\d\d)# setting (status) 
		   pre {
			  returned = event:attrs();
			  tokens = getTokens().encode({"pretty": true, "canonical": true});
			  vehicle_info = pds:get_item(namespace(), "vehicle_info")
							  .delete(["myProfilePhoto"])
							  .delete(["profilePhoto"])
					  .encode({"pretty": true, "canonical": true});
			  url =  ent:last_carvoyant_url;
			  params = ent:last_carvoyant_params;
			  type = event:type();

			  error_msg = returned{"content"}.decode() || {};

			  errorCode = error_msg{["error","errorCode"]} || "";
			  detail = error_msg{["error","detail"]} || "";
			  field_errors  = error_msg{["error","fieldErrors"]}
			                     .encode({"pretty": true, "canonical": true}) || [];
			  reason =  error_msg{["error","errorDisplay"]} || "";

			  attrs = event:attrs().encode({"pretty": true, "canonical": true});

	          owner = common:fleetChannel();

			  msg = <<
		Carvoyant HTTP Error (#{status}): #{event:attr('status_line')}

		// more here
		>>;

			}
			{
			  send_directive("carvoyant_fail") with
				sub_status = returned and
				error_code = errorCode and
				detail = detail and
			    reason = reason and
				field_errors = field_errors;
				
			}	
			fired {
			  error warn msg
			}
		  }


Then, we do this:

		rule handle_error {
			select when system error 
			pre {
				genus = event:attr("genus");
				species = event:attr("species") || "none";
				level = event:attr("level");
				rid = event:attr("error_rid");
				rule_name = event:attr("rule_name");
				msg = event:attr("msg");
				eci = meta:eci();
				session = CloudOS:currentSession() || "none";
				ent_keys = rsm:entity_keys().encode();
			    kre = meta:host();

				error_email = <<
	A Fuse error occured with the following details:
	  RID: #{rid}
	  Rule: #{rule_name}
	  Host: #{kre}

	  level: #{level}
	  genus: #{genus}
	  species: #{species}
	  message: #{msg}

	  eci: #{eci}
	  txn_id: #{meta:txnId()}
	  PCI Session Token: #{session}
	  RSM Entity Keys: #{ent_keys}
	>>;
			}

			{
				sendgrid:send(to_name, to_addr, subject, error_email);
			}
		    always {
		       raise test event error_handled for b16x12 
		      	  attributes
		     		{"rid": meta:rid(),
			     	 "attrs": event:attrs()
			        } 
				if event:attr("_test")
	    	} 
		}
	}










