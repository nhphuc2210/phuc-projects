
# **Python - LiteSQL**

## **JOB REQUIREMENTS**
<br />

    I have 3 spreadsheets which need to be joined, and found insights from.   
    
    Spreadsheet 1: 40,000 rows.  
    Data regarding shifts which employers have posted. Including whether the shifts were fulfilled or not.   
    
    Spreadsheet 2: 130,000 rows.  
    Data regarding employees selecting a shift. A shift can be selected multiple times in case the first employee canceled.   
    
    Spreadsheet 3: 80,000 rows.  
    Data regarding cancelations. A shift can be canceled multiple times if it was selected multiple times.   
    
    Only a subset of the data between the 3 sheets match each other.   
    
    Deliverables: 
    1) Find trends for the subset of data that overlaps.  
    2) Find trends for each sheet individually.  
    3) Identify and highlight which trends overlap.  


## **Definitions**



Each row in your shift data (cleveland_shifts.csv) is a shift; the following are helpful descriptions of columns within that dataset:

“Agent ID”: HCP ID

“Facility ID”: HCF ID

“Start”: The shift start time

Agent Req”: the type of HCP that is being requested for this shift

“End”: The shift end time

“Shift Type”: specifies if the shift is in the morning (AM), afternoon (PM), overnight (NOC), or custom (CUSTOM)

“Deleted”: Whether the shift was deleted

Note “deleted” means “cancelled by facility”

“Created At”: When the shift was created

“Charge”: Per hour charge rate

“Time”: How many hours the shift lasts

“Verified”: Indicates that the shift was worked, as confirmed by a signed timesheet


Each row in your cancellation logs (cleveland_cancel_log.csv) is a unique cancellation event; the following are helpful descriptions of columns within that dataset:


“Action”: The type of cancellation action

“WORKER_CANCEL”: The HCP cancelled a shift they booked

“NO_CALL_NO_SHOW”: The HCP cancelled a shift they booked after the shift commenced or otherwise did not show up to the shift and did not inform Clipboard or the facility about their absence

“Created At”: When the action took place

“Facility ID”: HCF ID

“Worker ID”: The ID of the HCP that was previously associated with the shift

“Shift ID”: The shift ID

“Lead Time”: The time from “action” to “shift start” (in hours)


Each row in your shift claim logs (cleveland_booking_logs.csv) is a unique booking event; the following are helpful descriptions for columns within that dataset:

Note that we only included claim actions for a subset of the date range in the "shifts" data. Thus, there are likely shifts that don't have associated claim actions. That's OK, we're only providing this data so you can observe HCP booking behavior.

“Action”: The type of booking action

"SHIFT_CLAIM": The HCP instantly booked the shift. As soon as they booked the shift, it was theirs.
