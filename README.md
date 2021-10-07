# hs_logger

This is the logger used by the MSL Humidity Standards team for calibrations and research. It is undergoing continuous improvement as part of BAU.

The logger has the following functionalities:
* Read and write to any instrument that has an {instrument}.json file using the instrument window of main_controller.py (NB: Currently can't load instruments directly. They must be in a job file first.)
* Log data for {job}.json files using the job window of main_controller.py
* Control jobs using an {autoprofile}.csv file on the Profile tab of the job window above
* Produce graphs of logged data
* Record files of logged data for later analysis

The software is started by running main_controller.py

# Instrument files

Instrument files consist of a dictionary containing at least the following details:
* instrument_id (STRING: The name the logger uses to refer to this instrument once it's imported)
* driver (STRING: What driver the instrument uses to read/write)
* operations  (DICTIONARY: Contents listed below.)

Specific drivers may require additional information. For instance, the generic_driver_visa_serial driver requires a port number, baudrate, and write_ and read_termination characters. Documentation of what additional details are required is included in the drivers. (NB: This information isn't currently in the drivers. It should be added.)

The operations dictionary contains every command that can be given to instrument. These are split into "read", "write", and "action". Each operation must contain the following:
* type (STRING: The first section of this string determines if this operation is a read, a write, or an action. Additional information here can be used by the driver.)
* name (STRING: The plain text name for the command for use in documentation.)
* id (STRING: This should be the same as the name of the operation in the dictionary. It is the function that is called by the logger to perform this operation.)
* details (STRING: A description of this specific operation for use in documentation.)
* command (STRING: The command that communicates the desired operation to the device.)

The following additional details are required if the operation is a read operation:
* transform_eq (LIST of (STRING,FLOAT,FLOAT,FLOAT,FLOAT): The equation used to generate the transformed data. The first datum can be used to tell certain drivers what equation the transform uses, such as "T" using a Callendar–Van Dusen equation. The next four numbers are the variables used in the transform equation.)
* rep_num (STRING: The name of the last valid calibration report for the particular operation, if appropriate. Otherwise, leave "".)
* check_date (STRING: The date of the last valid check for the particular operation (such as an ice point check), if appropriate. Otherwise, leave "".)

The following details are required if the operation is a write operation:
* check_set (STRING: The read operation that reads the value this operation writes to, if available. Otherwise, leave Otherwise, leave "".)
* check_actual (STRING: The read operation that reads the transducer this operation would attempt to control, if available. Otherwise, leave Otherwise, leave "".)

[THE STORE AND WRITE_ACTIONS]

# Job Files

# Autoprofile Files

# The Instrument Window

# The Job Window
* [HOW TO MAKE GRAPHS]
* [HOW TO USE A PROFILE]