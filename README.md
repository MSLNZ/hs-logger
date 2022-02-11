# hs_logger

This is the logger used by the MSL Humidity Standards team for calibrations and research. It is undergoing continuous improvement as part of BAU.

The logger has the following functionalities:
* Read and write to any instrument that has an {instrument}.json file using the instrument window of main_controller.py (NB: Currently can't load instruments directly. They must be in a job file first.)
* Log data for {job}.json files using the job window of main_controller.py
* Control jobs using an {autoprofile}.csv file on the Profile tab of the job window above
* Produce graphs of logged data
* Record files of logged data for later analysis

The software is started by running main_controller.py

***

# Instrument files

Instrument files consist of a dictionary containing at least the following details:
* instrument_id (STRING; The name the logger uses to refer to this instrument once it's imported)
* driver (STRING; What driver the instrument uses to read/write)
* operations  (DICTIONARY of (STRING: DICTIONARY of (STRING: VARIOUS)); Contents of this dictionary are listed below.)

Specific drivers may require additional information. For instance, the generic_driver_visa_serial driver requires a port number, baudrate, and write_ and read_termination characters. Documentation of what additional details are required is included in the drivers. (NB: This information isn't currently in the drivers. It should be added.)

The operations dictionary contains every command that can be given to the instrument. These are split into "read", "write", and "action". Each operation must contain the following:
* type (STRING; The first section of this string determines if this operation is a read, a write, or an action. Additional information here can be used by the driver, such as the read_multiple, read_store, and write_action commands detailed at the end of this section.)
* name (STRING; The plain text name for the command for use in documentation.)
* id (STRING; This should be the same as the key of this operation in the operations dictionary. It is the function that is called by the logger to perform this operation.)
* details (STRING; A description of this specific operation for use in documentation.)
* command (STRING; The command that communicates the desired operation to the device. Use "{}" in place of inputs in write commands.)

The following additional details are required if the operation is a read operation:
* transform_eq (LIST of (STRING,FLOAT,FLOAT,FLOAT,FLOAT); The equation used to generate the transformed data. The first datum can be used to tell certain drivers what equation the transform uses, such as "T" using a Callendar–Van Dusen equation. The next four numbers are the variables used in the transform equation.)
* rep_num (STRING; The name of the last valid calibration report for the particular operation, if appropriate. Otherwise, leave "".)
* check_date (STRING; The date of the last valid check for the particular operation (such as an ice point check), if appropriate. Otherwise, leave "".)

The following details are required if the operation is a write operation:
* check_set (STRING; The read operation that reads the value this operation writes to, if available. Otherwise, leave "".)
* check_actual (STRING; The read operation that reads the transducer this operation would attempt to control, if available. Otherwise, leave "".)

Some instruments use read_multiple/read_store commands or write_action commands. These are special functions that are detailed below.

read_multiple and read_store are connected commands that are used to speed up read/write times to instruments that allow them. This is accomplished by using a read_multiple operation to read a bunch of values at once, which are then written to an internal list referred to as the store. read_store operations then extract the desired data from this store instead of from the instrument itself. Because accessing the store takes considerably less time than communicating with an external instrument, this saves a lot of time.

write_action operations are used by the autoprofile system to perform actions on the system using a write command. This is accomplished using a dictionary of available action operations indexed by string. This string is set by the autoprofile, and the corresponding action operation is performed. Because write_action operations are write operations, they can have associated check_set and check_actual values. If they do, their keys will most likely be determined by the values produced by these check operations.

***

# Job Files

Job files consist of a dictionary containing at least the following details:
* job_name (STRING; The name the logger uses to refer to this job.)
* out_dir (STRING; The external directory that this job will write to. Normally an address in I:\\. If external recording isn't required, simply put "\\" and no connection will be established.)
* filenames (STRINGS; Seven file names must be included: _raw and _trans for each of datafile, points_file, and source_file, as well as a sensor_file. These filenames control where the data is put during logging. datafile contains all the recorded data, points_file contains each "point" taken, source_file contains the data that was converted into those points, and sensor_file contains relevant information, such as the calibration equations of the instruments. _raw contains the data as it was recorded, while _trans records that data after it has been transformed.)
* min_interval (INTEGER; The minimum number of minutes allowed between cycles. Can be 0.)
* time (INTEGER; Starting time. Normally 0.)
* instruments (DICTIONARY of (STRING: STRING); The instrument files that need to be used. The key of each entry should be the instrument_id of that instrument, while the data should be the filename of that instrument file including any path information required.)
* logged_operations (LIST of (STRING); The read operations that need to be used. Each should take the form of {instrument}.{operation}, where {instrument} is the instrument_id of the instrument being read and {operation} is the id of the read operation being performed.)
* details (DICTIONARY of (STRING: DICTIONARY of (STRING: STRING)); Additional details regarding instrument positions and other notable information. The outer-most dictionary uses instruments as keys, while the inner-most dictionaries use operations as keys. Only notable keys need to be filled in. If no relevant information needs to be recorded, this can be left as an empty dictionary.)
* references (DICTIONARY of (STRING: DICTIONARY of (STRING: VARIOUS)); Contains the reference "operations" that the logger will record. The outer-most dictionary uses the keys provided as the operations' names, while the inner-most dictionaries each include eight specific details which define the data values that will be associated their operation. The reference calculations take an initial reference humidity "hum" as well as reference pressure "p1", temperature "t1" and dew/frost state "df1" at this humidity, and then calculate the humidity at another point with reference pressure "p2", temperature "t2" and dew/frost state "df2", using an equation defined by "type". "hum", "p1", "p2", "t1", and "t2" are all STRINGS of the same form as detailed in logger_operations, indicating which operation defines their values. "df1" and "df2" are INTEGERS, with 0 being dew and 1 being frost. "type" is a STRING consisting of the type of humidity measurement being made and the type of humidity measurement being calculated. d represents a dew point, and h represents a relative humidity. The first letter in the string is what is being calculated, and the second letter is what is being provided. For instance, calculating a dew point from a relative humidity would have "type": "dh". If no references are needed, this can be left as an empty dictionary.)

***

# Autoprofile Files

Autoprofile files consist of comma delineated lines containing the following:
* filename (Must start with an "a". Suggested name is "a{start date}\_{client company name}\_{name of DUT}")
* write operation names (First three must be "Points", "Soak", and "Assured". Names are recommended to indicate both the instrument and operation being used in the write command.)
* write operation ids (First three should be left as "". Additional operations should take the form of {instrument}.{operation}, where {instrument} is the instrument_id of the instrument being written to and {operation} is the id of the write operation being performed.)
* values to write (An individual line is detailed below.)

Values should be as follows:
* Points (The number associated with this point. The first one should be "1", second "2", and so on.)
* Soak (The time, in minutes, that the logger should wait before trying to move to the next point. If no Assured is set, this will be approximately how long the logger waits between points. If Assured is set, this will be how long the logger waits before checking Assured.)
* Assured (The operation that Assured is trying to wait for. "0" or less is no Assured, "1" is the first instrument operation, "2" is the second, and so on. Only one value can be assured against at a time.)
* additional operations (The value that will be written to the instrument using this write command.)

No additional lines should be included after the last comma delineated line, nor should any additional commas be included at the end of lines 2 and onwards. Line 1, because it only contains the filename, can contain any number of superfluous characters after the first comma.

***

# The Instrument Window

(NB. Instrument window should have instrument name as the window name.)

(NB. Status should be implemented or removed.)

***

# The Job Window



* [HOW TO MAKE GRAPHS]
* [HOW TO USE A PROFILE]