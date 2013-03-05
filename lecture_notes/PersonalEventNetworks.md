
The lectures discusses 

1. Entity variables and persistent storage 
2. Entity-oriented event buses

## Entity Variables

The form-submit example ([a16x69.krl](/lecture_notes/krl/form_submit/a16x69.krl)) shows the following:

* initialize and populate rule pattern
* entity storage
* explicit events

<a href="./images/eventloop.jpg"><img src="../../../raw/master/lecture_notes/images/eventloop.jpg" alt="" style="width: 70%" /></a>


## Event Busses, Networks, and Clouds

<a href="./images/eventcloud.jpg"><img src="../../../raw/master/lecture_notes/images/eventcloud.jpg" alt="" style="width: 70%" /></a>

The following rulesets all listen for the <tt>thermostat:temperature</tt> event:

* [CT30 Thermostat service](/lecture_notes/krl/CT30_Thermostat_Service/a16x149.krl)
* [Temperature app](/lecture_notes/krl/Temperature_app/a16x164.krl)
* [Light Controller](/lecture_notes/krl/Hue_app/a16x166.krl)

What's important:

* Common event semantics create opportunities for interaction 
   - analogous to URLs
   - [Example Event Documentation](http://developer.kynetx.com/display/docs/CloudOS+Event+Protocol)
* Different rulesets see and react to common events, but are independent and loosely coupled 
